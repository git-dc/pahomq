#! /usr/bin/env python3

import time
import datetime

def stampGen(s):
    return datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")

def getkeys(msgs):
    keys = [key for key in msgs] 
    keys.remove("Time")
    return keys

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
            item=[stampGen(":".join(item))+datetime.timedelta(hours=-4)]
            print("modified: "+str(item[0])+", timezone: "+str(item[0].tzinfo))
            
        msgDict[header] = item[0]
    return msgDict
        
myMessage = '{"Time":"2018-05-16T16:02:38","ENERGY":{"Total":22.189,"Yesterday":0.790,"Today":0.529,"Period":0,"Power":44,"Factor":0.40,"Voltage":231,"Current":0.480}}'

#print(type(stampGen(s)))
message = convert_to_influx(myMessage)

s="2018-05-16T16:02:38"
print("original: "+str(stampGen(s))+", timezone: "+str(stampGen(s).tzinfo))
print("utc.....: "+str(datetime.datetime.utcnow())+", timezone: "+str(datetime.datetime.utcnow().tzinfo))



print (time.strftime("%z", time.gmtime()))
print(time.tzname)

def display(myList):
    print()
    for item in myList:
        print(item)
    print()
