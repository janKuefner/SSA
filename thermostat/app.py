import paho.mqtt.client as mqtt
import time #used to code sleep times for devices to safe battery

username = input("press ENTER to continue:")
print("weiter geht es")




import os  

hostname = "nebula_mosquitto_container" #example
#hostname = "localhost" #example
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
  print ('broker is up!')
else:
  print ('broker is down!')


print("Yolo") 
print("###")
print("###")
print("###")
print("###")


client = mqtt.Client()
#client.connect("localhost",6666,60)
client.connect("nebula_mosquitto_container",1883,60)
client.publish("/test", "yolo")
  


n=0
while True:
  n=n+1
  time.sleep(5)
  print (n)
  
