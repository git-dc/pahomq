#! /usr/bin/env python3

def convert_to_influx(message):

    msgDec = message.replace("{","").replace("}","").split(',"ENERGY":')
    
    subitems = msgDec[1].split(",")
    msgDec.pop(1)
    for item in subitems:
        msgDec.append(item)
    
    display(msgDec)
    
def display(myList):
    for item in myList:
        print(item)

    
myMessage = '{"Time":"2018-05-16T16:02:38","ENERGY":{"Total":22.189,"Yesterday":0.790,"Today":0.529,"Period":0,"Power":44,"Factor":0.40,"Voltage":231,"Current":0.480}}'
    
convert_to_influx(myMessage)
