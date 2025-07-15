import os

def create_default_env_file():
    """
    Creates a default .env file with placeholder values for API keys
    and default settings.
    """
    env_content = """# This file contains environment variables for your application.
# Fill in your actual API keys and customize default settings as needed.

# Debugging
DEBUG=True

# API Keys (IMPORTANT: Replace these with your actual keys)
MTA_API_KEY=your_mta_api_key_here
GOOGLE_CALENDAR_API_KEY=your_google_calendar_api_key_here
WEATHER_API_KEY=your_weather_api_key_here

# Default Settings
DEFAULT_WEATHER_LOCATION=New York
DEFAULT_SUBWAY_STATION=181st Street
DEFAULT_SUBWAY_LINE=ACE

# Default Latitude and Longitude (New York City coordinates)
DEFAULT_LATITUDE=40.7128
DEFAULT_LONGITUDE=-74.0060

# Add other configuration variables as needed
# EXAMPLE_VARIABLE=example_value
"""

    env_file_path = '.env'

    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"Successfully created default '{env_file_path}' file.")
        print("Please open the .env file and replace placeholder API keys with your actual keys.")
    except IOError as e:
        print(f"Error creating '{env_file_path}' file: {e}")

if __name__ == "__main__":
    create_default_env_file()