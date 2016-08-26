#!/usr/bin/python

import datetime
import Adafruit_BMP.BMP085 as BMP085
from influxdb import InfluxDBClient

def read_sensor():
	sensor = BMP085.BMP085()
	values = {}
	values['current_time'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
	values['temp'] = to_fahr(sensor.read_temperature())
	values['pressure'] = sensor.read_pressure()
	values['sea_pressure'] = sensor.read_sealevel_pressure()
	values['altitude'] = sensor.read_altitude()
	values['pi_temp'] = to_fahr(get_pi_temp())
	return values

def get_pi_temp():
	f = open('/sys/class/thermal/thermal_zone0/temp','r')
	pi_temp = float(f.read()) / 1000
	f.close
	return pi_temp

def to_fahr(temp_c):
	return ((9.0/5.0) * temp_c) + 32

def write_vals_to_influx(values):

	# --- MODIFY here to have your influx variables match your influx setup
	host = <your_influx_host_ip>
	port = <your_influx_port_eg_8086>
	user = <your_influx_user_name>
	password = <your_influx_user_pass>
	dbname = 'temp_pressure_v1'
	# --------------- END MODIFY ---------------------------------#

	json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "sensor": "BMP180",
            },
            "time": values['current_time'],
            "fields": {
                "value": values['temp']
            }
        },

        {
            "measurement": "temperature",
            "tags": {
                "sensor": "pi",
            },
            "time": values['current_time'],
            "fields": {
                "value": values['pi_temp']
            }
        },

        {
            "measurement": "sea_pressure",
            "tags": {
                "sensor": "BMP180",
            },
            "time": values['current_time'],
            "fields": {
                "value": values['sea_pressure']
            }
        },

        {
            "measurement": "pressure",
            "tags": {
                "sensor": "BMP180",
            },
            "time": values['current_time'],
            "fields": {
                "value": values['pressure']
            }
        }
	]

	client = InfluxDBClient(host, port, user, password, dbname)
	client.write_points(json_body)


def main():
	values = read_sensor()
	write_vals_to_influx(values)

if __name__ == '__main__':
    main()
