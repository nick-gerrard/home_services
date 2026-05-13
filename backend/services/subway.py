import datetime

import httpx
from google.protobuf.json_format import MessageToDict
from google.transit import gtfs_realtime_pb2

LINE_TO_GROUP: dict[str, str] = {
    "A": "ACE", "C": "ACE", "E": "ACE", "ACE": "ACE",
    "B": "BDFM", "D": "BDFM", "F": "BDFM", "M": "BDFM", "BDFM": "BDFM",
    "G": "G",
    "J": "JZ", "Z": "JZ", "JZ": "JZ",
    "N": "NQRW", "Q": "NQRW", "R": "NQRW", "W": "NQRW", "NQRW": "NQRW",
    "L": "L",
    "1": "1234567", "2": "1234567", "3": "1234567", "4": "1234567",
    "5": "1234567", "6": "1234567", "7": "1234567", "1234567": "1234567",
}

FEED_URLS: dict[str, str] = {
    "ACE": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
    "BDFM": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
    "G": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
    "JZ": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",
    "NQRW": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
    "L": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
    "1234567": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
}


async def get_arrivals(stop_id: str, line: str, num_trains: int = 5) -> list[dict]:
    group = LINE_TO_GROUP.get(line.upper())
    if not group:
        raise ValueError(f"Unknown subway line: {line!r}")

    url = FEED_URLS[group]
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    feed_dict = MessageToDict(feed)

    arrivals: list[dict] = []
    for entity in feed_dict.get("entity", []):
        if "tripUpdate" not in entity:
            continue
        trip = entity["tripUpdate"]
        route_id = trip["trip"].get("routeId", "?")

        for stop_update in trip.get("stopTimeUpdate", []):
            if stop_update.get("stopId") != stop_id:
                continue
            time_val = stop_update.get("arrival", {}).get("time")
            if not time_val:
                continue
            arrival_dt = datetime.datetime.fromtimestamp(int(time_val), tz=datetime.timezone.utc)
            minutes = int((arrival_dt - now).total_seconds() / 60)
            if minutes < 0:
                continue
            arrivals.append({"route": route_id, "minutes": minutes})

    arrivals.sort(key=lambda x: x["minutes"])
    return arrivals[:num_trains]
