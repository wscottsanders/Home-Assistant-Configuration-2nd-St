# Networked sensor script

import dht  
import tsl2561
import json 
from time import sleep 
from machine import I2C, Pin, unique_id
from umqtt.simple import MQTTClient 


if __name__ == "__main__":
    
    # Setup sensors 
    d = dht.DHT22(Pin(2))  #D4 on NodeMCU board is GPIO 2
    i2c = I2C(-1, Pin(5), Pin(4)) #D1 & D2 on NodeMCU board. 
    l = tsl2561.TSL2561(i2c)
    l.integration_time(402)    #Adjusts the length of exposure. 
    l.gain(16)              # Set to 1 or 16 but no values between.  16 is more sensitive.

    # Setup MQTT 
    broker = "192.168.1.64"    # ip address of computer running the broker.
    client_id = "multi_1"       # client id.
	
    client = MQTTClient(client_id, broker)
    client.connect()

    print("Connected to {}".format(broker))
        
    while True: 
        try: 

            # Take sensor measurement!s
            d.measure()
            
            try: 
                lux = l.read(autogain=True)
                raw_l, infrared = l.read(autogain=True, raw=True)
            except: 
                lux = 0.0
                raw_l, infrared = 0.0, 0.0

            fahrenheit = d.temperature()*9/5 + 32

            # Build JSON 
            data = {"lux": lux, "raw_light": raw_l, "infrared": infrared, "temperature": fahrenheit, "humidity": d.humidity()}
            json_data = json.dumps(data)
            
            # Publish to MQTT broker 
            client.publish('home-assistant/multi_1/multi_data', bytes(str(json_data), 'utf-8'))
            
            
            # Print sensor data - enable for debugging and to see if the sensor is collecting information properly. 
            print("\n *** Temperature ***") 
            print("Farenheit:  ", fahrenheit)
            print("Humidity:   ", d.humidity())
            print("\n *** Light ***")
            print("Lux:        ", lux)
            print("Vis. Light: ", raw_l)
            print("Infrared:   ", infrared)
            
            sleep(15)
        except: 
            try: 
                client.connect() 
            except: 
                pass 
                
        