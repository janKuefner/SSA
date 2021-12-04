import paho.mqtt.client as mqtt
import time


any_var = input("connect node to the Docker network - and then press Enter")
print("moving on...")

client = mqtt.Client()
client.connect("nebula_mosquitto_container",1883,60) #connect to broker


while True: #loop forever
  time.sleep(3) #device sleeps to save battery power
  client.publish("/temperature", "yolo")
  
