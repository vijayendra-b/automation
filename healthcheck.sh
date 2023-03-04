#!/usr/bin/env bash
# Environment Variables
# HUB_HOST
# BROWSER
# MODULE

echo "Checking if hub is ready - $SE_EVENT_BUS_HOST"

while [ "$( curl -s http://$SE_EVENT_BUS_HOST:4444/wd/hub/status | jq -r .value.ready )" != "true" ]
do
  echo "Current status of hub is - " $( curl -s http://$SE_EVENT_BUS_HOST:4444/wd/hub/status | jq -r .value.ready )
  sleep 1
done

pytest  -n $N_PROCESSES --dist=loadscope --alluredir=test_report/ $MODULE_NAME --ip=$SE_EVENT_BUS_HOST --browser=$BROWSER --ci_url=$CI_URL
