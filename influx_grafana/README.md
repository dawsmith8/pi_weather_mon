# Running InfluxDB and Grafana

For storing data from the weather station, I set up a basic Ubuntu box on which
I could run various [Docker]() containers

My build was a basic nuc or gigabyte brix with a 120GB SSD and 8GB of RAM.

Installing Docker: `curl -sSL https://get.docker.com/ | sh`
Then run `sudo usermod -aG docker <your username>` to make your life a little
easier when working with Docker rather than having to go to root or sudo all
the time.

A quick note- this project was done before Docker Swarm was a thing, one could
certainly look at using swarm to connect up these two containers.


### Making the InfluxDB container

First, I needed to have a place to write the data, InfluxDB seemed like a
fairly easy starting point.

On my Ubuntu host, I first made a /var/influxdb where my container would keep
its data - this way the influx data would live between restarts and upgrades
of the container.

Next with the files in [docker-influx](docker-influx), I made a basic container
to run influx - taking help from many of the samples available in DockerHub.
I made a ~/docker-influx directory with the above files then:

* Build the container image: `docker build . -t dawsmith8/influxdb`
* Start the container: ./start_influx.sh

### Making the Grafana container
