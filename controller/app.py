import paho.mqtt.client as mqtt
import time
import random #used to create ID
import os #used for clear screen

def create_ID():
      return("cont"+str(random.randrange(1001,9999)))

def on_message(client, userdata, msg):
      '''this callback function is triggered, when a message is received. It 
      disects the payload as per specification (see readme file). It checks if
      the information was received from a new node, if so it creates another 
      node object to store the values. Finally this method stores the 
      information of the payload in the correct node object
      '''
      recevied_string = (msg.payload.decode()) #store received payload
      type = (msg.topic[5:9]) #get the type from MQTT topic
      ID=(recevied_string[4:8]) #disect the payload into ID
      command=(recevied_string[8:11]) #disect the payload into command
      value=(recevied_string[16:19]) #actuator / sensor value
      print(recevied_string)
      print(type)
      print(ID)
      print(command)
      print(value) 
      print("----------")
      

class Controller:
      def __init__(self):
            '''this object doesn`t have any attributes'''
            
      def render_gui(self):
            '''this methods renders a GUI of a controller'''
            print("render GUI in here")
            #os.system('printf "\033c"') #clears screen
            

class Node:
      def __init__(self, ID, type, value, last_seen):
            self.ID = ID 
            self.type = type #e.g. thermometer or lamp
            self.value = value #e.g. degree Celsius or lamp on
            self.last_seen = last_seen #time elapsed since last transmission 
                 


nodes = [] #create an empty list where all node objects are stored
#nodes.append( Node ("1","thermo","22","1"))
#nodes.append( Node ("1","lala","22","1"))
controller = Controller() #create a Controller object
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
  client.subscribe("home/temp")
  client.on_message = on_message
  client.loop_start()
  
  
'''

while True:
      print(create_ID())
      '''