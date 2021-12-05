import paho.mqtt.client as mqtt
import time
import random #used to create ID


def create_ID():
      return("cont"+str(random.randrange(1001,9999)))

def on_message(client, userdata, msg):
      print(msg.payload.decode())
      

class Controller:
      def __init__(self, node_IDs):
            '''node_IDs is an array that stores all IDs of the nodes'''
            self.node_IDs = node_IDs
            
      def update_temperature_from_nodes(self):
            '''this methods updates temperatures from nodes and prints them'''
            print("Yolo")
            client.subscribe("home/temp")
            client.on_message = on_message
            client.loop_start()
                 

controller = Controller([]) #create a Controller object
client_id = create_ID() #create a random client ID
client = mqtt.Client(client_id) #create a MQTT client object


'''the following line of code is used to delay this programm / the node till 
the user connected this node to the Docker network. This is essential, since a 
MQTT connection to the broker can only be successfull, if the node is in the 
same network as the broker'''
any_var = input("integrate this node to the Docker network & then press Enter")


client.connect("nebula_mosquitto_container",1883,60) #connect to broker
print("MQTTS started")



while True: #loop forever
  time.sleep(1) #communication sleeps to save battery power
  controller.update_temperature_from_nodes()
'''

while True:
      print(create_ID())
      '''