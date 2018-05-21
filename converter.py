#! /usr/bin/env python3

import time
import datetime
    
def display(myList):
    print()
    for item in myList:
        print(item)
    print()

def stampGen(s):
    return str(time.mktime(datetime.datetime.strptime(s,"%Y-%m-%d:%H:%M:%S").timetuple())+14400)

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
            item[0] = item[0].replace("T",":")
            item=[stampGen(':'.join(item))[:-2]+"000000000"]
            
        msgDict[header] = item[0]
    return msgDict
        
myMessage = '{"Time":"2018-05-16T16:02:38","ENERGY":{"Total":22.189,"Yesterday":0.790,"Today":0.529,"Period":0,"Power":44,"Factor":0.40,"Voltage":231,"Current":0.480}}'
    
message = convert_to_influx(myMessage)
print(getkeys(message))
