import os
import requests
from google.cloud import pubsub_v1
import json

# --- Configuration ---
# Your main Pub/Sub topic where the individual records will stream
PUBLISH_TOPIC_ID = "usgs-earthquake-data" 
USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.geojson"
# ---------------------

def fetch_and_publish_usgs_data(event, context):
    """
    Cloud Function triggered by a Pub/Sub message.
    Fetches GeoJSON, extracts features, and publishes them individually.
    """
    # The CloudEvents format for Pub/Sub events on Cloud Run includes the project ID
    # in the context, but it's simpler to rely on the environment variable set by GCP.
    project_id = os.environ.get('GCP_PROJECT') 
    if not project_id:
        print("Error: GCP_PROJECT environment variable not set.")
        return

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, PUBLISH_TOPIC_ID)

    try:
        # 1. Fetch the data from USGS
        print(f"Fetching data from: {USGS_API_URL}")
        response = requests.get(USGS_API_URL, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        features = data.get("features", [])

        # 2. Iterate and Publish each GeoJSON feature to the data stream topic
        publish_futures = []
        for feature in features:
            # Pub/Sub requires data to be a bytestring
            message_data = json.dumps(feature).encode('utf-8')
            
            # Publish and collect the future for confirmation
            future = publisher.publish(topic_path, data=message_data)
            publish_futures.append(future)
        
        # Wait for all publishes to complete
        for future in publish_futures:
            future.result() 

        print(f"Successfully published {len(features)} earthquake records.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
