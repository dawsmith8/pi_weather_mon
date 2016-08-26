#!/usr/bin/python

import datetime
import Adafruit_BMP.BMP085 as BMP085

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
	pi_temp = float(f.read())
	f.close
	return pi_temp

def to_fahr(temp_c):
	return ((9.0/5.0) * temp_c) + 32

def write_vals_tolog(values):
	log_date = datetime.datetime.now().strftime("%Y%m%d")
	log_name = "{0}_temps_pressures.log".format(log_date)
	#print 'using logname: {0}'.format(log_name)
	log_path = "/home/pi/logs/{0}".format(log_name)
	#print values.keys()
	f = open(log_path, 'a')
	line_out = "{current_time:s}, temp:{temp:0.2f}, pressure:{pressure:0.2f}, pi_temp:{pi_temp:0.2f}\n".format(**values)
	f.write(line_out)
	f.close()

def main():
	values = read_sensor()
	write_vals_tolog(values)

if __name__ == '__main__':
    main()
