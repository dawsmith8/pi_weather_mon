#!/bin/bash

docker run -d -p 3001:3000 \
  -v /var/grafana/grafana-docker/data:/var/lib/grafana \
  -v /var/grafana/grafana-docker/log:/var/log/grafana \
  -v /var/grafana/grafana-docker/etc:/etc/grafana \
  -e "GF_SERVER_ROOT_URL=http://grafana.ubuntu-dev1"  \
  dawsmith8/grafana
