import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish #import the publish1
import time

#import time
import os
import sys
import logging
import json


import broadlink

SUBSCRIBE = 'broadlink/+/command'
MQTT_SERVER = os.getenv('MQTT_SERVER')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

############
def on_connect(client, userdata,flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	print("Subscribing to topic ",SUBSCRIBE)
	client.subscribe(SUBSCRIBE)

def on_message(client, userdata, message):
 print("Message received: " ,str(message.payload.decode("utf-8")))
 print("-Topic: ",message.topic)
 print("-QOS: ",message.qos)
 print("-Retain: ",message.retain)
 #print(message.topic.split('/'))
 	
 try:
	#print(message.payload.json())
 	json_decode=str(message.payload.decode("utf-8","ignore"))
 	print("Decoding Json")
 	parsed_json=json.loads(json_decode)
 except json.decoder.JSONDecodeError:
    print("Error passing JSON")
    return
	
 MAC_ADDR = str(message.topic.split('/')[1])
 print("Broadlink: "+MAC_ADDR)
 #print("Command: "+parsed_json[0])
 
	#print("Value: "+str(parsed_json["value"]))

 send_command(MAC_ADDR, parsed_json)
 
def send_command(mac, parsed_json):
	print("Searching for Broadlink devices")
	devs = broadlink.discover(timeout=5)
	if len(devs) == 0:
		print("No Devices Found")
		return

	#dev = next(bl for bl in devs if mac in (None, '') or bl.mac == mac)
        ## OlegJktu change original code. Delet MAC control. Because Beok have mac 34:ea:34:70
	dev = devs[0]
	for bl in devs:
		#hex_data = binascii.hexlify(bl.mac)
		strmac = ':'.join(format(s, '02x') for s in bl.mac[::-1])
		if strmac == mac.lower():
			print('Broadlink with mac 02x', strmac, ' found ', bl.host)
			dev = bl
		else:
			print('Device with mac ', strmac, ' found ', bl.host)
			dev = bl
			
	dev.auth()

	print()
	print(dev.type)
	time.sleep(1)
	print()
	
	for key, value in parsed_json.items():
		print (key)
		if key == 'get_temp':
			data = dev.get_temp()
			print ("Received temp: ", data)
			pub = 'broadlink/'+mac+'/temp'
			print ("Publishing to:", pub)
			publish.single(pub, data, hostname=MQTT_SERVER, auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD})
		# Do the thing
		elif key == 'get_external_temp':
			print ('get_external_temp')
			data = dev.get_external_temp()
			print ("Received external temp: ", data)
			pub = 'broadlink/'+mac+'/exttemp'
			print ("Publishing to:", pub)
			publish.single(pub, data, hostname=MQTT_SERVER, auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD})
		# Do yet another thing
		elif key == 'get_full_status':
			data = dev.get_full_status()
			print ("Received status: ", data)
			pub = 'broadlink/'+mac+'/status'
			print ("Publishing to:", pub)
			publish.single(pub, json.dumps(data), hostname=MQTT_SERVER, auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD})
		# Do yet another thing
		elif key == 'set_mode':
			print ('get_external_temp')
		# Do yet another thing
		elif key == 'set_advanced':
			print ('get_external_temp')
		# Do yet another thing
		elif key == 'switch_to_auto':
			print ('get_external_temp')
		# Do yet another thing
		elif key == 'switch_to_manual':
			print ('get_external_temp')
		# Do yet another thing
		elif key == 'set_temp':
			dev.set_temp(value)
			print ('set_temp')
		# Do yet another thing
		elif key == 'set_power':
			dev.set_power(value)
		# Do yet another thing
		elif key == 'set_time':
			print ('get_external_temp')
		# Do yet another thing
		elif key == 'set_schedule':
			print ('get_external_temp')
		# Do yet another thing
		else:
			print("Unknown command, getting temp as default")
			data = dev.get_temp()
			print ("Received temp: ", data)
			pub = 'broadlink/'+mac+'/temp'
			print ("Publishing to:", pub)
			publish.single(pub, data, hostname=MQTT_SERVER, auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD})
		# Do the default
 
########################################
#broker_address="192.168.1.184"
print("Starting MQTT")
client = mqtt.Client("HB") #create new instance
client.on_message=on_message #attach function to callback
client.on_connect=on_connect
print("Connecting to Broker: "+MQTT_SERVER)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_SERVER) #connect to broker
#client.loop_start() #start the loop
client.loop_forever()

#print("Publishing message to topic","chromecast/TV/command/dashcast")
#client.publish("chromecast/TV/command/dashcast","{'"+DASHBOARD_URL+"', 'true'}")
#time.sleep(4) # wait
#client.loop_stop() #stop the loop
