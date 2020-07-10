import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from time import sleep


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)         # Read output from PIR motion sensor 1
    GPIO.setup(14, GPIO.IN)        # Read output from PIR motion sensor 2 

    # Broker's ip/network address
    broker = '192.168.1.115'
    state_topic = 'home-assistant/pir_1/presence'
    delay = .1

    client = mqtt.Client("pir1-client")
    client.connect(broker)
    client.loop_start()

    prev_state = 0 
    while True:
        if GPIO.input(4) == 1 or GPIO.input(14) ==1: 
            presence = 1
        else: 
            presence = 0 
        
        # When output from motion sensor is low.

        if presence == 0:
            print "No intruder: ", presence
            if presence != prev_state: 
                client.publish(state_topic, presence)
            sleep(delay)

        #When output from motion sensor is HIGH
		elif presence == 1:               
            print "Intruder: ", presence
            if presence != prev_state:
                client.publish(state_topic, presence)
            sleep(delay)

        prev_state = presence