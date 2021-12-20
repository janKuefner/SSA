import paho.mqtt.client as mqtt  # used for MQTT protocol
import time  # used to simulate IoT delays
import os  # used for clear screen
import random  # used to create ID


def create_ID():
    '''this function is used to give the node a random ID at startup of the
    node. This is to simulate that a node has a hardware bound ID. The
    function is random and not one set ID is used, so this code can be run in
    Docker multiple times to simulate as many noddes. This is not as a real
    IoT system would be designed. It is however good for the simulation of a
    manifold IoT system in Docker'''
    return("temp"+str(random.randrange(1001, 9999)))


def on_connect(client, userdata, flags, rc):
    print("Connected flags", str(flags), "result code", str(rc))
    '''The broker acknowledgement will generate a callback (on_connect). To make 
    sure that connection attempt was successful a function to handle this callback 
    needs to be set up before creating the connection."client" is the client instance
    for this callback, "userdata" is the private user data as set in Client(), "flags" 
    are response flags sent by the broker and "rc" is the connection result which can
    indicate the following values: 0: Connection successful 1: Connection refused - 
    incorrect protocol version 2: Connection refused - invalid client identifier 
    3: Connection refused - server unavailable 4: Connection refused - bad username 
    or password 5: Connection refused - not authorised 6-255: Currently unused.'''

def on_message(client, userdata, msg):
    '''this callback function is triggered, when a message is received.It
    disects the payload as per specification (see readme file). If there is a
    message for this node that calls for action (e.g. change set temeprature)
    this node will do so, if the message doesn`call for action or is not for
    this node. No action will happen (e.g. set temperature will remain as is)
    '''
    string_rcvd = (msg.payload.decode())  # store received payload
    # type_rcvd = (msg.topic[5:9]) #get the type from MQTT topic
    # ID_rcvd=(string_rcvd[0:8]) #disect the payload into ID
    command_rcvd = (string_rcvd[8:11])  # disect the payload into command
    value_rcvd = (string_rcvd[16:18])  # actuator / sensor value
    recipient_ID_rcvd = (string_rcvd[18:26])  # recipient of this message
    if command_rcvd == "set" and recipient_ID_rcvd == client_id:
        thermometer.set_temperature = int(value_rcvd)


class Thermometer:
    def __init__(self, set_temperature, current_temperature, payload):
        '''set_temperature stores the value given by the controller the
        heating is set to'''
        self.set_temperature = set_temperature
        self.current_temperature = current_temperature
        self.payload = payload

    def render_gui(self):
        '''this methods renders a GUI of a thermometer'''
        print("sending...")
        time.sleep(0.2)  # show sending for a short time
        os.system('printf "\033c"')  # clears screen
        '''print essential data from a thermometer'''
        print("This node has the following ID: ", client_id)
        print()
        print("Set temperature:", self.set_temperature)
        print("Current temperature: ", self.current_temperature)

    def create_payload(self):
        '''the following if statement is to simulate that the measured
        temperature is sometimes not as the set temperature. The temperature
        fluctuation is not real, but ideal to check, showcase and verify a IoT
        home system simulated in Docker. The payload is assembled as per
        specification within the readme file'''
        random_offset = random.randrange(-3, 3)
        self.current_temperature = self.set_temperature + random_offset
        self.payload = client_id + "pub-----" + str(self.current_temperature)


client_id = create_ID()  # create a random client ID
client = mqtt.Client(client_id)  # create a MQTT client object
thermometer = Thermometer(0, 13, "lalala")  # create a thermometer object


'''the following line of code is used to delay this programm / the node till
the user connected this node to the Docker network. This is essential, since a
MQTT connection to the broker can only be successfull, if the node is in the
same network as the broker'''
any_var = input("integrate this node to the Docker network & then press Enter")

client.tls_set("/app/certs/ca.crt")
client.tls_insecure_set(True)

client.username_pw_set(username="jan", password="nebula2")
'''username_pw_set() is a helper method of the Paho client that implements 
username and password restrictions.Authentication credentials are transmitted 
in clear text, and not secure without TSL encription.However,is is an easy way
of restricting access to a broker.'''
print("Authenticating...")

client.on_connect = on_connect # attach function to callback

client.connect("mosquitto_container", 8883, 60)  # connect to broker
print("Success. MQTTS started")


while True:  # loop forever
    client.subscribe("home/temp", qos=1)  # subscribe with QoS of 1
    '''time.sleep is used to simulate a IoT device, since sleeping safes
    battery'''
    time.sleep(5)
    thermometer.create_payload()  # create payload
    client.publish("home/temp", thermometer.payload)  # publish payload
    client.on_message = on_message  # check for message from broker
    client.loop_start()  # necessary for MQTT
    '''render GUI, likely tiny LCD, if it was a real device'''
    thermometer.render_gui()
