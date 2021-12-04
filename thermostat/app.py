import paho.mqtt.client as mqtt
import time


any_var = input("integrate this node to the Docker network & then press Enter")
print("starting MQTTS...")

client = mqtt.Client()
client.connect("nebula_mosquitto_container",1883,60) #connect to broker
print("MQTTS started")


while True: #loop forever
  time.sleep(3) #device sleeps to save battery power
  client.publish("/temperature", "yolo")
  