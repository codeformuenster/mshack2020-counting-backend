import json
import os
import requests
import pytz

from datetime import datetime, timedelta

tz = pytz.timezone("Europe/Berlin")

# Api docs hystreet: https://static.hystreet.com/apidocs

# curl -H "Content-Type: application/vnd.hystreet.v1" -H "X-API-Token: xyz" https://hystreet.com/api/locations | jq '.[] | select(.city == "Münster")'
# ids to import: 117, 296, 100

locations = {
    "100": {
        "lat": 51.960632,
        "lon": 7.625117,
    },
    # "296": {
    #     "lat": 51.9636,
    #     "lon": 7.6294,
    # },
    # "117": {
    #     "lat": 51.9586,
    #     "lon": 7.6273,
    # },
}

hystreet_url = "https://hystreet.com/api/locations"
hystreet_token = os.getenv("HYSTREET_TOKEN")

counting_backend_url = "https://counting-backend.codeformuenster.org/counts/"

# datetime.now().astimezone(tz).replace(hour=1,minute=0,second=0,microsecond=0).isoformat()

now = datetime.now().astimezone(tz)

# param_from = now.replace(hour=now_hour - 1,minute=0, second=0, microsecond=0).isoformat()
# param_to = now.replace(hour=now_hour, minute=0, second=0, microsecond=0).isoformat()
param_from = (now - timedelta(minutes=6)).replace(second=0, microsecond=0).isoformat()
param_to = (now - timedelta(minutes=1)).replace(second=0, microsecond=0).isoformat()
param_resolution = "hour"


def fetch_hystreet(id):
    params = {"from": param_from, "to": param_to, "resolution": param_resolution}
    headers = {
        "X-API-Token": hystreet_token,
        "Content-Type": "application/vnd.hystreet.v1",
    }
    r = requests.get(
        f"{hystreet_url}/{id}",
        params=params,
        headers=headers,
    )
    return r.json()


def post_counts(lat, lon, count, timestamp):
    payload = {
        "lat": lat,
        "long": lon,
        "count": count,
        "timestamp": timestamp,
    }
    print(json.dumps(payload))
    r = requests.post(counting_backend_url, json=payload)
    return r.text


if __name__ == "__main__":
    for id, mocks in locations.items():
        print(id)
        result = fetch_hystreet(id)
        post_result = post_counts(
            mocks["lat"],
            mocks["lon"],
            result["statistics"]["timerange_count"],
            result["metadata"]["measured_to"],
        )

        print(result)
        print(post_result)
