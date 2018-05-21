#! /usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe("vaponic/tele/SENSOR")

    
def on_message(client, userdata, msg):
    print("received a message on topic " + msg.topic)
    #use UTC as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    isfloatValue=False
    try:
        #convert the string to a float so that it is stored as a number and not as a string in the db
        val=float(message)
        isfloatValue=True
    except:
        print("Could not convert " + message + " to a float value")
        isfloatValue=False
    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val))

        json_body = [
            {
                "measurement":msg.topic,
                "time":receiveTIme,
                "fields":
                {
                    "value":val
                }
            }
        ]
        dbclient.write_points(json_body)
        print("Finished writing to InfluxDB")

# set up a client for influxdb
dbclient = InfluxDBClient('localhost',8086,'admin','admin','sensordata')

# initialize the mqtt client that should connect to the mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect("localhost",1883,60)
        connOK=True
    except:
        connOK=False
    time.sleep(2)


# blocking loop to the mosquitto broker
client.loop_forever()

