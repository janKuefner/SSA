import paho.mqtt.client as mqtt #used to do MQTTS connection
import time #used to create a timer
import os #used to clear screen in Gui class
import random #used to create a random number



class Thermometer:
      def __init__(self, set_temperature, current_temperature):
        '''set_temperature stores the value given by the controller the  
        heating is set to'''
        self.set_temperature = set_temperature
        self.current_temperature = current_temperature
        
      def render(self):
        '''this methods renders a GUI of a thermometer'''
        print("Set temperature:", self.set_temperature )
        print("Current temperature: ", self.current_temperature)
        print("----------------------------")
        
      def measure_temperature(self):
        '''this method simulates that the measured temperature is sometimes not 
        as the set temperature.'''
        if random.randrange(0,5) == 3:
          self.current_temperature = self.set_temperature +1
        else:
          self.current_temperature = self.set_temperature
            
      
thermometer = Thermometer (20, 13) #create a thermometer object with some values
client = mqtt.Client() #create a MQTT client object


'''the following line of code is used to delay this programm / the node till 
the user connected this node to the Docker network. This is essential, since a 
MQTT connection to the broker can only be successfull, if the node is in the 
same network as the broker'''
any_var = input("integrate this node to the Docker network & then press Enter")

client.connect("nebula_mosquitto_container",1883,60) #connect to broker

'''
a=0
while a<40:
  gui.measure_temperature()
  #print(gui.set_temperature)
  gui.render()
  a=a+1
  time.sleep(0.2)
'''

while True: #loop forever
  time.sleep(3) #communication sleeps to save battery power
  thermometer.measure_temperature()
  thermometer.render()
  client.publish("home/temp", thermometer.current_temperature)
