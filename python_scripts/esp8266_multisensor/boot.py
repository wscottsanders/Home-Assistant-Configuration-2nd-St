# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()
import network


def do_connect(essid, pw):
    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, pw)
        while not sta_if.isconnected():
            print "Having trouble connecting..."
			pass
    print('network config:', sta_if.ifconfig())

do_connect("ATTFnI4dbA", "wfy65%=u?squ")   # passes essid and pw to connect fuction.