import paho.mqtt.client as paho
import time
# import ssl


client = paho.Client()
any_var = input()  # here I connect this container to the docker network

client.tls_set("/app/certs/ca.crt")
client.tls_insecure_set(True)
client.connect("nebula_mosquitto_container", 8883, 60)
time.sleep(5)
client.publish("home/temp", "yolo")
