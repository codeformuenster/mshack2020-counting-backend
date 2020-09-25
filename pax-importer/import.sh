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
URL=http://localhost:8080/counts/
#URL=https://counting-backend.codeformuenster.org/counts/

# jq data transformation
DEVICE_JQ_QUERY=".[] | select(.longitude!=null) | .device_id"


while read -r payload
do
  curl -H "Content-type: application/json" -d "$payload" "$URL"
  sleep 0.05
done  < <(jq -c "${JQ_QUERY}" "${INPUT}")


# jq data transformation
JQ_QUERY=".[] | select(.longitude!=null) | { count: .wifi, timestamp: .time }"


while read -r payload
do
  curl -H "Content-type: application/json" -d "$payload" "$URL"
  sleep 0.05
done  < <(jq -c "${JQ_QUERY}" "${INPUT}")
