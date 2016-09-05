# Running InfluxDB and Grafana

For storing data from the weather station, I set up a basic Ubuntu box on which
I could run various [Docker](https://www.docker.com) containers

My build was a basic nuc or gigabyte brix with a 120GB SSD and 8GB of RAM.

Installing Docker: `curl -sSL https://get.docker.com/ | sh`
Then run `sudo usermod -aG docker <your username>` to make your life a little
easier when working with Docker rather than having to go to root or sudo all
the time.

A quick note- this project was done before Docker Swarm was a thing, one could
certainly look at using swarm to connect up these two containers.


### Making the InfluxDB container

First, I needed to have a place to write the data, [InfluxDB](https://influxdata.com)
seemed like a fairly easy starting point.

On my Ubuntu host, I first made a /var/influxdb where my container would keep
its data - this way the influx data would live between restarts and upgrades
of the container.

Next with the files in [docker-influx](docker-influx), I made a basic container
to run influx - taking help from many of the samples available in DockerHub.
I made a ~/docker-influx directory with the above files then:

* Build the container image: `docker build . -t dawsmith8/influxdb`
* Start the container: ./start_influx.sh

#### Setting up InfluxDB:
With the influx container running, go to http://<your_ip or host>:8083 to get
to the influx web page.  Note you may wish to change/set admin passwords at
this point, as they are the defaults...

Make a starter db to store your data - using the saved queries you should be
able to make a new db - for example temp_pressure - note this name as you will
need it when setting up your graphs in grafana and when you modify your [python](../raspberry_pi/temp_pressure_toinflux.py#L30-L34)
that writes from the RaspberyPi.

### Making the Grafana container

[Grafana](http://grafana.org) was a similar process to the influx container to setup.
There were a few more directories to make, you can see these noted in the
volume mounts in the start-grafana.sh

```
mkdir -p /var/grafana/grafana-docker/data
mkdir -p /var/grafana/grafana-docker/log
mkdir -p /var/grafana/grafana-docker/etc
```

I also picked a server URL alias to pass to the container, this can also
just be your IP:

``"GF_SERVER_ROOT_URL=http://grafana.<hostname>"  ``

Again with a directory in ~/docker-grafana -

* Build the container image: `docker build . -t dawsmith8/grafana`
* Start the container: ./start_influx.sh

#### Setting up Grafana

With the grafana container running, you should be able to go to
http://<host or ip>:3001 to get to the Grafana UI.  Note again, the default admin/password
is set, you may wish to change those.

From there you will need to add data sources to Grafana so it knows where InfluxDB
is:

InfluxData Source:
```
Type is InfluxDB 0.9.x
URL is http://<ip or hostname>:8086   Acess is proxy
Database is the db name you picked above setting up InfluxDB
User and password for influx should be what you chose when setting up the DB.
```

You can now make a new dashboard in Grafana using this new data source.

A sample would be like:
* Select mean(value) From pressure
* Go to the Time Range tab and pick a range you would like - eg 24 hours or 7 days.
