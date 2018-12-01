# MQTT-Hysen, Beok, Floureon, Decdeal
A Broadlink Thermostat docker controlled using MQTT

Credit to [madmod/dashcast-docker](https://github.com/madmod/dashcast-docker), used as a base for this docker.

This docker is a gateway to control the Broadlink Themostat using MQTT and will publish status messages

## Device compatibility
This must work whith wifi thermostats of different chines brand like Hysen, Beok, Floureon, Decdeal. If you can see thermostat in app broadlink (but can not control it) it look like it would be compability. If you can control thermostat from Beok Home or Room heat app (android) the thermostat is compability.
Beok models Beok BOT-313WiFi-WH and Beok TDS22 WP WiFi are compability.

## Discovery and control

Using MQTT you can control the Broadlink Themostat using the following topic. `MAC` is the mac address of the device in the format 00:11:22:aa:bb:cc.

	broadlink/MAC/command
  
Publish a json array with the command and value
`broadlink/MAC/command`, e.g. `{"set_power":1}`.

The following commands are currently working;

- get_temp `Value is undefined for this. This command will force the current temperature to be publsihed to broadlink/MAC/temp`
- get_external_temp `Value is undefined for this. This command will force the current external temperature to be publsihed to broadlink/MAC/exttemp`
- get_full_status `Value is undefined for this. This command will force the status to be publsihed to broadlink/MAC/status as JSON`
- set_temp `Value is numeric between 0 - 35 (currently tested on celcius).`
- set_power `Value is 1 or 0# Set device on(1) or off(0), does not deactivate Wifi connectivity.`
- default or blank `This will default to get_temp`

## How to use this image

```console
$ docker run --name MQTT-Hysen --restart unless-stopped --net=host -e MQTT_SERVER="192.168.0.10" -e MQTT_USERNAME="user" -e MQTT_PASSWORD="password" -d mukowman/MQTT-Hysen
```
This will start a python based MQTT client listening on topic broadlink/+/command.
Any messages received will be sent to an active Broadlink Thermostat
Folder /app in Docker have files and script inside it.
