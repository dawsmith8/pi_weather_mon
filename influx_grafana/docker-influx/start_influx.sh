#! /bin/bash
docker run -d --volume=/var/influxdb:/data -p 8083:8083 -p 8086:8086 -p 25826:25826/udp 'dawsmith8/influxdb'
