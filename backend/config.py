import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'  # Default to True if not set

    # API Keys
    MTA_API_KEY = os.getenv('MTA_API_KEY')
    GOOGLE_CALENDAR_API_KEY = os.getenv('GOOGLE_CALENDAR_API_KEY')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

    # Default settings
    DEFAULT_WEATHER_LOCATION = os.getenv('DEFAULT_WEATHER_LOCATION', 'New York')
    DEFAULT_SUBWAY_STATION = os.getenv('DEFAULT_SUBWAY_STATION', '181st Street')
    DEFAULT_SUBWAY_LINE = os.getenv('DEFAULT_SUBWAY_LINE', 'ACE')

    DEFAULT_LATITUDE = os.environ.get('DEFAULT_LATITUDE', 40.7128)  # Default to New York City
    DEFAULT_LONGITUDE = os.environ.get('DEFAULT_LONGITUDE', -74.0060) # Default to New York City


    # Add other configuration variables as needed