# backend/subway/services.py

import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import datetime
from flask import current_app  # To access Flask config

API_URLS = {
    "ACE": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
    "BDFM": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
    "G": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
    "JZ": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",
    "NQRW": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
    "L": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
    "1234567": r"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
}

def get_next_train_arrivals(line, stop_id, num_trains=5):
    """Retrieves and sorts arrival times for a given stop ID."""
    try:
        url = API_URLS[line]
    except KeyError:
        current_app.logger.error(f"Invalid line choice: {line}")
        return {}  # Return empty dictionary for consistency

    try:
        response = requests.get(url)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        feed_dict = MessageToDict(feed)

        arrivals = []  # List of (arrival_time, route_id) tuples

        for entity in feed_dict.get('entity', []):  # Handle case where 'entity' might be missing
            if 'tripUpdate' in entity:
                trip_update = entity['tripUpdate']
                route_id = trip_update['trip'].get('routeId', "Unknown Train Line")

                for stop_time_update in trip_update.get('stopTimeUpdate', []): # Handle case where 'stopTimeUpdate' might be missing
                    if stop_time_update.get('stopId') == stop_id:
                        if 'arrival' in stop_time_update and 'time' in stop_time_update['arrival']:
                            arrival_time = stop_time_update['arrival']['time']
                            if isinstance(arrival_time, str):
                                try:
                                    arrival_time = int(arrival_time)
                                except ValueError:
                                    continue

                            arrival_time_dt = datetime.datetime.fromtimestamp(arrival_time, tz=datetime.timezone.utc) # Be timezone aware
                            arrivals.append((arrival_time_dt, route_id))  # Add tuple to list

        # Sort by arrival time
        arrivals.sort(key=lambda x: x[0])

        # Take the next num_trains
        next_trains = {}
        for i in range(min(num_trains, len(arrivals))):  # Handle fewer than num_trains
            arrival_time, route_id = arrivals[i]
            train_id = f"{route_id}{i+1}"
            next_trains[train_id] = arrival_time
        return next_trains

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Request Error for line {line}: {e}")
        return {}
    except Exception as e:
        current_app.logger.error(f"General Error processing line {line}: {e}")
        return {}


def format_time(arrivals):
    """Formats datetime objects to HH:MM AM/PM strings."""
    formatted_arrivals = {}
    if not arrivals:
        return {}

    try:
        for key, dt_object in arrivals.items():
            if isinstance(dt_object, datetime.datetime):
                # Convert to local timezone for display
                local_arrival_time = dt_object.astimezone(datetime.timezone(datetime.timedelta(hours=-4))) # Assuming EDT
                formatted_arrivals[key] = local_arrival_time.strftime("%I:%M %p") # 12-hour format with AM/PM
            else:
                current_app.logger.warning(f"Value for key '{key}' is not a datetime object. Skipping.")
    except Exception as e:
        current_app.logger.error(f"Error formatting time: {e}")
        return {}

    return formatted_arrivals