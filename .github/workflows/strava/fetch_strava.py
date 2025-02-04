import requests
import json
import os

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def get_access_token():
    url = "https://www.strava.com/oauth/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=params).json()
    return response["access_token"]

# Fetch latest Strava activity
def get_latest_activity():
    access_token = get_access_token()
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers).json()
    
    if response:
        latest = response[0]  # Most recent activity
        return {
            "name": latest["name"],
            "distance": latest["distance"] / 1000,  # Convert to km
            "time": latest["moving_time"] // 60,  # Convert to minutes
            "type": latest["type"],
        }
    return None

# Update README file
def update_readme(activity):
    if activity:
        content = f"""
### 🚴 My Latest Strava Activity

**{activity['name']}**  
🏃 {activity['distance']:.2f} km | ⏱️ {activity['time']} min | 🏋️ {activity['type']}

_Last updated: now_
"""
        with open("README.md", "w") as f:
            f.write(content)

activity = get_latest_activity()
update_readme(activity)
