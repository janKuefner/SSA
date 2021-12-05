import paho.mqtt.client as mqtt
import time
import random #used to create ID
import os #used for clear screen

nodes = [] #create an empty list where all node objects are stored

def create_ID():
      return("cont"+str(random.randrange(1001,9999)))

def on_message(client, userdata, msg):
      '''this callback function is triggered, when a message is received. It 
      disects the payload as per specification (see readme file). It checks if
      the information was received from a new node, if so it creates another 
      node object to store the values. Finally this method stores the 
      information of the payload in the correct node object
      '''
      string_rcvd = (msg.payload.decode()) #store received payload
      type_rcvd = (msg.topic[5:9]) #get the type from MQTT topic
      ID_rcvd=(string_rcvd[4:8]) #disect the payload into ID
      command_rcvd=(string_rcvd[8:11]) #disect the payload into command
      value_rcvd=(string_rcvd[16:19]) #actuator / sensor value
      '''check if node is known already'''
      for node in nodes:
            if (node.ID == ID_rcvd): #check if a node object exists with the ID
                  node.value = value_rcvd #if so update value send
                  node.last_seen = 0 #set time when last seen to zero
                  break
      else: #if not in list create a new object node an append it to nodes
            new_node = Node(ID_rcvd, type_rcvd, value_rcvd, 0)
            nodes.append(new_node)     
      

class Controller:
      def __init__(self):
            '''this object doesn`t have any attributes'''
            
      def render_gui(self):
            '''this methods renders a GUI of a controller'''
            os.system('printf "\033c"') #clears screen
            for node in nodes:
                  print("--------------------------------")
                  print("Heating No. {0} set to XYZ °C".format(node.ID))
                  print("{0} °C - measured {1} sec ago".format(node.value, node.last_seen))
                  #print(node.ID)
                  #print(node.type)
                  #print(node.value)
                  #print(node.last_seen)            
            

class Node:
      def __init__(self, ID, type, value, last_seen):
            self.ID = ID 
            self.type = type #e.g. thermometer or lamp
            self.value = value #e.g. degree Celsius or lamp on
            self.last_seen = last_seen #time elapsed since last transmission 
                 


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
      delay_time = 1 #in sec used to simulate a real IoT system
      time.sleep(delay_time) #device sleeps to simulate a real IoT system
      for node in nodes:
            node.last_seen = node.last_seen + delay_time #increment timer
      client.subscribe("home/temp")
      client.on_message = on_message
      controller.render_gui()
      client.loop_start()
