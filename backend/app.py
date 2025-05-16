from flask import Flask
from flask_cors import CORS
from subway.routes import subway_bp
from events.routes import events_bp
from weather.routes import weather_bp
from config import Config  # Assuming you'll create this

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

app.register_blueprint(subway_bp, url_prefix='/api/subway')
app.register_blueprint(events_bp, url_prefix='/api/events')
app.register_blueprint(weather_bp, url_prefix='/api/weather')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0')