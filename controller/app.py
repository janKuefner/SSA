import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, msg):
      print(msg.payload.decode())      
      


any_var = input("integrate this node to the Docker network & then press Enter")
print("starting MQTTS...")

client = mqtt.Client()
client.connect("nebula_mosquitto_container",1883,60) #connect to broker
print("MQTTS started")



client.subscribe("home/temp")
while True: #loop forever
  #time.sleep(1) #communication sleeps to save battery power
  #print("controller here, still working...")
  
  client.on_message = on_message
  client.loop_start()