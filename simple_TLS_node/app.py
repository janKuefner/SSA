import paho.mqtt.client as paho #used for MQTT protocol
import time #used to simulate IoT delays
import ssl


           
 
client = paho.Client() #create a MQTT client object

any_var = input("integrate this node to the Docker network & then press Enter")




'''


client.tls_set("/app/certs/ca.crt", tls_version=ssl.PROTOCOL_TLSv1_1)
client.tls_insecure_set(True) 



client.connect("nebula_mosquitto_container",8883,60) #connect to broker
time.sleep(3)

while True:
      client.publish("home/temp", "yolo") #publish payload
      time.sleep(1)


'''





client.connect("nebula_mosquitto_container",1883,60) #connect to broker
time.sleep(3)

while True:
      client.publish("home/temp", "yolo") #publish payload
      time.sleep(10)
  
