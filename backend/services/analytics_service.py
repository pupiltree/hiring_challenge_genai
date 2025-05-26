import json
import os
from pathlib import Path

# Define the path to the analytics data file
DATA_DIR = Path(__file__).parent.parent / 'data'
ANALYTICS_FILE = DATA_DIR / 'analytics.json'

# Ensure the data directory exists
DATA_DIR.mkdir(exist_ok=True)

def track_event(event_type, ad_id):
    """Track an event (e.g., ad generation, A/B test selection) and increment its count."""
    data = {}
    if ANALYTICS_FILE.exists():
        try:
            with open(ANALYTICS_FILE, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupted JSON file
            data = {}

    if event_type not in data:
        data[event_type] = {}
    if ad_id not in data[event_type]:
        data[event_type][ad_id] = 0
    data[event_type][ad_id] += 1

    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_analytics():
    """Retrieve the current analytics data."""
    if not ANALYTICS_FILE.exists():
        return {}
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty dict if file is corrupted 