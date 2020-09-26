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

# datetime.now().astimezone(tz).replace(hour=1,minute=0,second=0,microsecond=0).isoformat()


# param_from = now.replace(hour=now_hour - 1,minute=0, second=0, microsecond=0).isoformat()
# param_to = now.replace(hour=now_hour, minute=0, second=0, microsecond=0).isoformat()
# param_from = (now - timedelta(minutes=6)).replace(second=0, microsecond=0).isoformat()
# param_to = (now - timedelta(minutes=1)).replace(second=0, microsecond=0).isoformat()


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


    now = datetime.now().astimezone(tz).replace(hour=0, minute=0,second=0, microsecond=0)


    day = 0

    for id, mocks in locations.items():
        param_from = (now - timedelta(days=(day + 1))).replace(hour=0, minute=0,second=0, microsecond=0).isoformat()
        param_to = (now - timedelta(days=(day))).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

        print(id)
        print(param_from)
        print(param_to)

        day = day + 1



        # result = fetch_hystreet(id, param_from, param_to)
        # with open(f"./laser_import/data/{mocks['name']}_{param_from}_{param_to}.json", "w") as f:
        #     # print(json.dumps(result, ensure_ascii=False))
        #     json.dump(result, f)

        # for

        # post_result = post_counts(
        #     mocks['name'],
        #     result["statistics"]["timerange_count"],
        #     result["metadata"]["measured_to"],
        # )

        # print(result)
        # print(post_result)
