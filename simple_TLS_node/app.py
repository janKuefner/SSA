import paho.mqtt.client as mqtt #used for MQTT protocol
import time #used to simulate IoT delays
import ssl

print("simple TLS app")
    
def on_message(client, userdata, msg):
      print(msg.payload.decode()) 
      
      
def on_log(client, userdata, level, buf):
      print("log: ",buf)
            
 
client = mqtt.Client() #create a MQTT client object

any_var = input("integrate this node to the Docker network & then press Enter")

'''
while True:
      print("yolo")
      time.sleep(2)
'''


'''callback functions'''
client.on_message = on_message #check for message from broker
client.on_log=on_log
'''TLS parameters'''
client.tls_set("/app/certs/ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
#client.tls_set("/app/certs/client.crt")
client.tls_insecure_set(True)
'''TLS connect, subscribe'''
client.connect("LAPTOP-J6SF4LLV",8883,60) #connect to broker 
client.connect("nebula_mosquitto_container",8883,60) #connect to broker
client.subscribe("home/temp")
print("MQTTS started") 
'''publish'''
client.publish("home/temp", "yolo") #publish payload
'''MQTT LOOP'''
client.loop_start() #loops MQTT commands
time.sleep(5) #used to simulate a IoT device, since sleeping safes battery :)
  
