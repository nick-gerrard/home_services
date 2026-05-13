import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WMO_DESCRIPTIONS: dict[int, str] = {
    0: "Clear",
    1: "Mostly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime Fog",
    51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
    56: "Freezing Drizzle", 57: "Heavy Freezing Drizzle",
    61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
    66: "Freezing Rain", 67: "Heavy Freezing Rain",
    71: "Light Snow", 73: "Snow", 75: "Heavy Snow", 77: "Snow Grains",
    80: "Rain Showers", 81: "Rain Showers", 82: "Heavy Showers",
    85: "Snow Showers", 86: "Heavy Snow Showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ Hail", 99: "Thunderstorm w/ Hail",
}


async def get_weather(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        "timezone": "America/New_York",
        "forecast_days": 1,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()

    data = response.json()
    current = data["current_weather"]
    daily = data["daily"]

    current_code = current.get("weathercode", 0)
    daily_code = daily["weathercode"][0] if daily.get("weathercode") else current_code

    return {
        "temperature": round(current["temperature"]),
        "wind_speed": round(current["windspeed"]),
        "description": WMO_DESCRIPTIONS.get(current_code, "Unknown"),
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
        "daily_description": WMO_DESCRIPTIONS.get(daily_code, "Unknown"),
    }
