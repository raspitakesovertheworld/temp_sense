import os, time, sys
import httplib, urllib, signal
import RPi.GPIO as GPIO


os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")
base_path="/sys/bus/w1/devices/"

#GPIO.cleanup()


def get_temp(device):
	tfile = open("/sys/bus/w1/devices/"+device+"/w1_slave")
	text = tfile.read()
	tfile.close()
	temperature_data = text.split()[-1]
	temperature = float(temperature_data[2:])
	temperature = temperature / 1000
	return temperature

def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))


def post_thingspeak(dict):
	cpu = getCPUtemperature()


	params1 = urllib.urlencode(dict)     
	print params1
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	try:
		conn.request("POST", "/update", params1, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
		conn.close()

			
	except:
		print  "connection failed!"                                                                                                                                      






dirs = os.listdir(base_path)
                                                                                                                                                                                                                                                                                                                                                     
#main look, runs forever
while True == True:
	dict={}
	i=1
	for element in dirs:
        	if element != "w1_bus_master1":
                	print element
                	dict["field"+str(i)]=get_temp(element)
			i = i + 1
	dict["field"+str(i)]=getCPUtemperature()
     
	dict["key"]="8M22NZN4KY2YV06D"


	post_thingspeak(dict)
	
	time.sleep(300)

	
