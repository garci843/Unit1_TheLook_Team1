import json
import requests
from datetime import datetime, timedelta
from google.cloud.pubsub_v1 import PublisherClient

publisher = PublisherClient()

PROJECT_ID = "mgmt467-4889"
TOPIC = "earthquake-streaming"
TOPIC_PATH = f"projects/{PROJECT_ID}/topics/{TOPIC}"

# choose your minimum magnitude
MIN_MAG = 2.5   # change to 3, 4, 5, etc.

def parse(request):

    # compute starttime = 30 days ago
    starttime = (datetime.utcnow() - timedelta(days=1)).isoformat()

    # build USGS API request
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson"
        f"&orderby=time"
        f"&starttime={starttime}"
        f"&minmagnitude={MIN_MAG}"
    )

    # fetch data
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    features = data.get("features", [])

    numProcessed = 0

    for feature in features:
        properties = feature.get("properties", {}) or {}
        geometry = feature.get("geometry", {}) or {}
        coordinates = geometry.get("coordinates", []) or []

        flattened_row = {
            "event_type": feature.get("type"),
            "id": feature.get("id"),

            "mag": properties.get("mag"),
            "place": properties.get("place"),
            "time": properties.get("time"),
            "updated": properties.get("updated"),
            "url": properties.get("url"),
            "detail": properties.get("detail"),
            "status": properties.get("status"),
            "tsunami": properties.get("tsunami"),
            "sig": properties.get("sig"),
            "net": properties.get("net"),
            "code": properties.get("code"),
            "ids": properties.get("ids"),
            "sources": properties.get("sources"),
            "types": properties.get("types"),
            "nst": properties.get("nst"),
            "dmin": properties.get("dmin"),
            "rms": properties.get("rms"),
            "gap": properties.get("gap"),
            "magType": properties.get("magType"),
            "event_class": properties.get("type"),
            "title": properties.get("title"),

            "geometry_type": geometry.get("type"),
            "longitude": coordinates[0] if len(coordinates) > 0 else None,
            "latitude": coordinates[1] if len(coordinates) > 1 else None,
            "depth": coordinates[2] if len(coordinates) > 2 else None,
        }

        row = json.dumps(flattened_row)

        publisher.publish(
            TOPIC_PATH,
            data=row.encode("utf-8")
        )
        numProcessed += 1

    return json.dumps(
        {"events_sent": numProcessed, "min_magnitude": MIN_MAG}
    )
