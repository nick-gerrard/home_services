# backend/subway/routes.py

from flask import Blueprint, jsonify, request, current_app
from .services import get_next_train_arrivals, format_time

subway_bp = Blueprint('subway', __name__)

@subway_bp.route('/arrivals')
def subway_arrivals():
    station_id = request.args.get('stop_id')
    line = request.args.get('line', current_app.config.get('DEFAULT_SUBWAY_LINE'))

    if not station_id:
        return jsonify({"error": "Missing 'stop_id' parameter"}), 400
    if not line:
        return jsonify({"error": "Missing 'line' parameter"}), 400

    arrivals = get_next_train_arrivals(line.upper(), station_id) # Assuming stop_id is case-sensitive
    formatted_arrivals = format_time(arrivals)

    return jsonify({
        "station_id": station_id,
        "line": line.upper(),
        "arrivals": formatted_arrivals
    })