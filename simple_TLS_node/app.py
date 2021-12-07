import paho.mqtt.client as mqtt #used for MQTT protocol
import time #used to simulate IoT delays
import os #used for clear screen
import random #used to create ID


    
def on_message(client, userdata, msg):
      print(msg.payload.decode()) 
            
 
client = mqtt.Client() #create a MQTT client object


any_var = input("integrate this node to the Docker network & then press Enter")


client.connect("nebula_mosquitto_container",1883,60) #connect to broker
print("MQTTS started")


while True: 
  client.subscribe("home/temp") 
  time.sleep(5) #used to simulate a IoT device, since sleeping safes battery :)
  client.publish("home/temp", "yolo") #publish payload
  print("published")
  client.on_message = on_message #check for message from broker
  client.loop_start() #necessary for MQTT
  
