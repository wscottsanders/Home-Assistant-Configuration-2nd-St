__author__ = 'Scott'

import time
import paho.mqtt.client as mqtt
from os import system

def on_connect(mosq, obj, rc):
    client.subscribe('ir', 0)
    print "Connection Response Code: ", str(rc)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

def on_message(mosq, obj, msg):
    global message
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    cmd = msg.payload
    system(cmd)

if __name__ == "__main__":

    # Broker's ip/network address
    broker = '192.168.1.64'

    # Creating a client.
    client = mqtt.Client("tyr")

    # Assign event callbacks
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    # Connect to broker.
    client.connect(broker)

    # Start the network loop.
    client.loop_forever()