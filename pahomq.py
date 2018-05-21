#! /usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient

def stampGen(s):
    return str(time.mktime(datetime.datetime.strptime(s,"%Y-%m-%d:%H:%M:%S").timetuple())+14400)

def convert_to_influx(message):
    junk = ["{","}",'"','ENERGY:']
    measurements=[]
    tags=''
    msgDict = {}
    
    for thing in junk: message = message.replace(thing,"")
    msgDec = [item.split(":") for item in message.split(',')]    
    
    for item in msgDec:
        header = item.pop(0)
        if len(item)>1:
            item[0] = item[0].replace("T",":")
            item=[stampGen(':'.join(item))[:-2]+"00000000"]
            
        msgDict[header] = item[0]
    return msgDict

        
def on_connect(client, userdata, flags, rc):
    print("mosquitto connected with result code " + str(rc))
    client.subscribe("vaponic/tele/SENSOR")

    
def on_message(client, userdata, msg):
    print("received a message on topic " + msg.topic)
    #use UTC as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    msgs=convert_to_influx(message)
    keys = [key for key in msgs]
    keys.remove("Time")
    for key in keys:
        isfloatValue=False
        try:
            #convert the string to a float so that it is stored as a number and not as a string in the db
            
            val=float(msgs[key])
            isfloatValue=True
        except:
            print("Could not convert " + message + " to a float value")
            isfloatValue=False
        if isfloatValue:
            print(str(receiveTime) + ": " + key + " " + str(val))
            json_body = [
                {
                    "measurement":key,
                    #"time":msgs["Time"],
                    "time":receiveTime,
                    "fields":
                    {
                        "value":msgs[key]
                    }
                }
            ]
            dbclient.write_points(json_body)
            print("Finished writing to InfluxDB")

# set up a client for influxdb
dbclient = InfluxDBClient('localhost',8086,'admin','admin','mydb')

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

