#!/bin/bash

# Input file
# a json file containing data like this:
# [
#  {
#    "latitude": 51.958209,
#    "longitude": 7.638576,
#    "time": "2020-09-18T09:59:05.156974612Z",
#    "wifi": 195
#  },
#  ...
# ]
INPUT=mshack-data-3d.json

# Url to post data to
#URL=http://localhost:8080
URL=https://counting-backend.codeformuenster.org

# create devices..
curl -H "Content-type: application/json" -d '{"id":"ttgo-beam","lat":51.958209,"lon":7.638576}' "$URL/devices/"

echo

# jq data transformation
JQ_QUERY=".[] | select(.longitude!=null) | { count: .wifi, timestamp: .time, device_id: .device_id }"

while read -r payload
do
  curl -H "Content-type: application/json" -d "$payload" "$URL/counts/"
  sleep 0.01
  echo
done  < <(jq -c "${JQ_QUERY}" "${INPUT}")
