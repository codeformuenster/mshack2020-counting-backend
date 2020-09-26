import json
import os
import pytz
import requests
import time

from datetime import datetime, timedelta

tz = pytz.timezone("Europe/Berlin")

# Api docs hystreet: https://static.hystreet.com/apidocs

# curl -H "Content-Type: application/vnd.hystreet.v1" -H "X-API-Token: xyz" https://hystreet.com/api/locations | jq '.[] | select(.city == "Münster")'
# ids to import: 117, 296, 100

locations = {
    "100": {
        "name": "hystreet_ms_rohtenburg_100",
        "lat": 51.960632,
        "lon": 7.625117,
    },
    "296": {
        "name": "hystreet_ms_alterfischmarkt_296",
        "lat": 51.9636,
        "lon": 7.6294,
    },
    "117": {
        "name": "hystreet_ms_ludgeristrasse_117",
        "lat": 51.9586,
        "lon": 7.6273,
    },
}

hystreet_url = "https://hystreet.com/api/locations"
hystreet_token = os.getenv("HYSTREET_TOKEN")

counting_backend_url = "https://counting-backend.codeformuenster.org"


def fetch_hystreet(id, param_from, param_to):
    params = {"from": param_from, "to": param_to, "resolution": "hour"}
    headers = {
        "X-API-Token": hystreet_token,
        "Content-Type": "application/vnd.hystreet.v1",
        "User-Agent": "mshack2020-hystreet-importer",
    }
    r = requests.get(
        f"{hystreet_url}/{id}",
        params=params,
        headers=headers,
    )
    return r.json()


def post_counts(device_id, count, timestamp):
    payload = {
        "device_id": device_id,
        "count": count,
        "timestamp": timestamp,
    }
    r = requests.post(f"{counting_backend_url}/counts/", json=payload)
    return r.text


def post_device(id, lat, lon):
    payload = {
        "lat": lat,
        "lon": lon,
        "id": id,
    }
    r = requests.post(f"{counting_backend_url}/devices/", json=payload)
    return r.text


if __name__ == "__main__":
    # register devices
    if False:
        for id, mocks in locations.items():
            r = post_device(mocks["name"], mocks["lat"], mocks["lon"])
            print(r)

    now = (
        datetime.now().astimezone(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    )

    for diff in range(1):
        for id, mocks in locations.items():
            param_from = (
                (now - timedelta(days=(diff + 1)))
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .isoformat()
            )
            param_to = (
                (now - timedelta(days=(diff)))
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .isoformat()
            )

            print(id)
            print(param_from)
            print(param_to)

            result = fetch_hystreet(id, param_from, param_to)
            with open(
                f"./laser_import/data/{mocks['name']}_{param_from}_{param_to}.json", "w"
            ) as f:
                json.dump(result, f, ensure_ascii=False)

            for m in result["measurements"]:
                post_result = post_counts(
                    mocks["name"],
                    m["pedestrians_count"],
                    m["timestamp"],
                )

                print(post_result)
        print("---- sleeping 5 seconds before continuing")
        time.sleep(5)
