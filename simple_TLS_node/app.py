import paho.mqtt.client as paho
import time


def on_message(client, userdata, msg):
    print(msg.payload.decode())


client = paho.Client()
any_var = input()  # here I connect this container to the docker network

client.tls_set("/app/certs/ca.crt")
client.tls_insecure_set(True)
client.connect("mosquitto_container", 8883, 60)
# client.connect("172.18.0.2", 8883, 60)
while True:
    time.sleep(1)
    client.publish("home/temp", "yolo")
    client.subscribe("home/temp")
    client.on_message = on_message
    client.loop_start()
