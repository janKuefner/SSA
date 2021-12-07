import paho.mqtt.client as mqtt #used for MQTT protocol
import time #used to simulate IoT delays
import random #used to create ID
import os #used for clear screen
import sys, select #used to break out the while loop


delay_time = 1 #in sec used to simulate a real IoT system
nodes = [] #create an empty list where all node objects are stored


def create_ID():
      '''this function is used to give the node a random ID at startup of the 
      node. This is to simulate that a node has a hardware bound ID. The 
      function is random and not one set ID is used, so this code can be run in 
      Docker multiple times to simulate as many noddes. This is not as a real 
      IoT system would be designed. It is however good for the simulation of a 
      manifold IoT system in Docker'''
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
      ID_rcvd=(string_rcvd[0:8]) #disect the payload into ID
      command_rcvd=(string_rcvd[8:11]) #disect the payload into command
      value_rcvd=(string_rcvd[16:18]) #actuator / sensor value
      recipient_ID_rcvd=(string_rcvd[18:26]) #recipient of this message
      '''add received string to the correct node - if node new create a new 
      entry within the nodes list'''
      for node in nodes:
            if (node.ID == ID_rcvd): #check if a node object exists with the ID
                  node.value = value_rcvd #if so update value send
                  node.last_seen = 0 #set time when last seen to zero
                  break
      else: #if not in list create a new object node an append it to nodes
            '''the node to be appended may not be this controller, since
            this controller shall not be listed as node to controll via MQTTS by
            this controller.'''
            if (ID_rcvd != client_id): #only append when not this controller
                  new_node = Node(ID_rcvd, type_rcvd, value_rcvd, 0, 0)
                  nodes.append(new_node)  
                  
                  
def on_publish(client,mid,result):
      '''this callback function is started when the broker returns an ACK 
      message. ACK messages are only send by broker with QoS 1 or QoS 2 (for 
      more information see readme file)
      a result larger 0 indicates that the message was sent. Note result is 
      incremented by the broker'''             
      if result > 0:
            print()
            print("Message successfully sent to broker")
      pass   


class Controller:
      def __init__(self):
            '''this object doesn`t have any attributes. But some methods :)'''
            
      def update_idle_timer_of_nodes(self):
            '''this methods increments the idle timer of a node. If a message is
            received from a node. The timer is set to 0. This setting to 0 is 
            done in the on_message callback function'''
            for node in nodes:
                  node.last_seen = node.last_seen + delay_time #increment timer
            
      def render_gui_that_shows_values_of_node(self):
            '''this methods renders a GUI of a controller, that shows the values
            of all connected nodes'''
            os.system('printf "\033c"') #clears screen
            print ("This node has the following ID: ", client_id) 
            print ()
            print ("Here are the connected nodes:")
            for node in nodes:
                  print("--------------------------------")
                  print("Heating No.:" ,node.ID)
                  print("Current temperature:", node.value) 
                  print("Current set value:",node.set_value)
                  print("Temperature last measured:", node.last_seen)
            print("--------------------------------")
            print ("")
            print ("Press Enter to set actuator (e.g. thermostat) values")
      
      def render_gui_that_lets_the_user_change_set_values(self):
            '''this methods renders a GUI of a controller, where the user can 
            set values e.g. set heating 3432 to 22 degree Celsius'''
            os.system('printf "\033c"') #clears screen
            n = 0
            for node in nodes:
                  print("--------------------------------")
                  print ("-", n ,"-")
                  print ("Node ID: ", node.ID)
                  print ("Node type: ", node.type)
                  print ("Current set value: ", node.set_value)
                  n = n + 1
            print("--------------------------------")
            print()
            '''In the following a user can pick a node. The inpout is validated 
            so non existing nodes or strings as input cannot be provided'''
            print ("Press 0 to", (len(nodes)-1) ,"& hit ENTER to select a node, where you want to change set value")
            while True:
                  print()
                  try:
                        sensor_chosen = int(input ())
                        if 0 <= sensor_chosen and sensor_chosen < len(nodes):
                              break
                        else: 
                              print ("Please provide a number between 0 and", (len(nodes)-1))
                  except:
                        print("Please provide a number")
            print ("Enter new set value")
            while True:
                  print()
                  try:
                        new_set_value = int(input ())
                        if 0 <= new_set_value < 100:
                              break
                        else: 
                              print ("Please provide a number between 0 and 99")
                  except:
                        print("Please provide a number")  
            if 0 <= new_set_value < 10:
                  new_set_value_two_characters = "0" + str(new_set_value)
            else:
                  new_set_value_two_characters = str(new_set_value)
            nodes[sensor_chosen].set_value = new_set_value_two_characters
            
      def transmit_set_values(self):
            '''this method is changing set values at all nodes by publishing 
            payloads as per specification of transmission within the readme file
            ''' 
            for node in nodes:
                  payload = client_id + "set-----" + str(node.set_value) + str(node.ID)
                  #payload = "cont7837set-----99temp4839"
                  client.publish("home/temp", payload, qos=1) #publish payload
            

class Node:
      '''in this Node class all information recevived from the broker is stored
      to the respective node. The node objects are stored in a nodes list. At 
      the beginning of the programm this list is empty. When receiving info
      from the broker on a node not yet within the list the list is updated. 
      The update of the list is done in the Controller Class by a controller 
      object that is created.'''
      def __init__(self, ID, type, value, last_seen, set_value):
            self.ID = ID 
            self.type = type #e.g. thermometer or lamp
            self.value = value #e.g. degree Celsius or lamp on
            self.last_seen = last_seen #time elapsed since last transmission
            self.set_value = set_value #e.g. 20 degree Celsius or light on 
                 

'''create some objects necessary for the programm to run'''
client_id = create_ID() #create a random client ID
controller = Controller() #create a Controller object
client = mqtt.Client(client_id) #create a MQTT client object


'''the following line of code is used to delay this programm / the node till 
the user connected this node to the Docker network. This is essential, since a 
MQTT connection to the broker can only be successfull, if the node is in the 
same network as the broker'''
any_var = input("integrate this node to the Docker network & then press Enter")


'''the following connects you to the broker and subsrcibes to relevant topics 
of the broker'''
client.connect("nebula_mosquitto_container",1883,60) #connect to broker
client.subscribe("home/temp")
print("MQTTS started")


'''The follow double loop (inner loop and outer loop) controls the programm flow
of the controller. The inner loop, that updates idle timers of nodes, renders a 
GUI that shows current values of node connected, checks for transmitted messages
is looping till an interrupt. When the interrupt is triggered a different GUI
is displayed where the user can change settings of devices'''
while True: #outer loop, which loops forever            
      while True: #inner loop, which loops till Enter is pressed
            time.sleep(delay_time) #device sleeps to simulate a real IoT system
            controller.update_idle_timer_of_nodes() #update idle timers
            '''the following function is a callback function that gets activated
            per every message available at the broker for this node'''
            client.on_message = on_message 
            controller.render_gui_that_shows_values_of_node() #render GUI
            client.loop_start() #necessary for MQTT
            '''the following stops the inner loop, if enter is pressed'''
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                  line = input()
                  break
      '''in the outer loop the user sees a different GUI once that GUI method
      completes. The programm jumps back to the inner loop'''
      controller.render_gui_that_lets_the_user_change_set_values() 
      controller.transmit_set_values()
      '''the following function is a callback function that gets activated per 
      every ACK message from the broker for this node. Note: ACK messages are 
      only returned by the broker in QoS 1 or QoS 2 - see readme file for more 
      information'''
      client.on_publish = on_publish
      '''the following delay is to show if ACK was received in this GUI before 
      jumping to the other GUI again. A jump would rather confuse the user, so 
      feedback is therfore provided in the settings GUI driven by the outer 
      loop'''
      time.sleep(3) 
