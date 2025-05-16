from flask import Blueprint, jsonify, request, current_app
import requests

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/current')
def get_current_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units', 'imperial')  # Default to Fahrenheit

    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'current_weather': True,
        'temperature_unit': 'celsius' if units == 'metric' else 'fahrenheit',
        'windspeed_unit': 'ms' if units == 'metric' else 'mph',
        'precipitation_unit': 'mm' if units == 'metric' else 'inch'
    }

    if lat:
        params['latitude'] = lat
    else:
        params['latitude'] = current_app.config.get('DEFAULT_LATITUDE')

    if lon:
        params['longitude'] = lon
    else:
        params['longitude'] = current_app.config.get('DEFAULT_LONGITUDE')

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        current_weather = weather_data.get('current_weather', {})
        temperature = current_weather.get('temperature')
        wind_speed = current_weather.get('windspeed')
        wind_direction = current_weather.get('winddirection')
        weather_code = current_weather.get('weathercode')
        timestamp = current_weather.get('time')

        # Map weather codes to descriptions and icons (simplified)
        weather_description, weather_icon = get_weather_interpretation(weather_code)

        formatted_data = {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
            "description": weather_description,
            "icon": weather_icon,
            "timestamp": timestamp
        }

        return jsonify(formatted_data)

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching weather data: {e}")
        return jsonify({"error": f"Failed to fetch weather data: {e}"}), 500
    except Exception as e:
        current_app.logger.error(f"Error processing weather data: {e}")
        return jsonify({"error": f"Error processing weather data: {e}"}), 500

def get_weather_interpretation(weather_code):
    # Simplified mapping - you can expand this for more detailed conditions
    if weather_code in [0]:
        return "Clear sky", "01d"
    elif weather_code in [1, 2, 3]:
        return "Mainly clear, partly cloudy, and overcast", "02d"
    elif weather_code in [45, 48]:
        return "Fog and depositing rime fog", "50d"
    elif weather_code in [51, 53, 55]:
        return "Drizzle", "09d"
    elif weather_code in [56, 57]:
        return "Freezing Drizzle", "09d"
    elif weather_code in [61, 63, 65]:
        return "Rain", "10d"
    elif weather_code in [66, 67]:
        return "Freezing Rain", "13d"
    elif weather_code in [71, 73, 75]:
        return "Snow", "13d"
    elif weather_code in [77]:
        return "Snow grains", "13d"
    elif weather_code in [80, 81, 82]:
        return "Rain showers", "09d"
    elif weather_code in [85, 86]:
        return "Snow showers", "13d"
    elif weather_code in [95]:
        return "Thunderstorm", "11d"
    elif weather_code in [96, 99]:
        return "Thunderstorm with hail", "11d"
    else:
        return "Unknown", "01d"