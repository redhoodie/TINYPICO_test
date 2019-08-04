import gc
import uos
from flashbdev import bdev

try:
    if bdev:
        uos.mount(bdev, '/')
except OSError:
    import inisetup
    vfs = inisetup.setup()

gc.collect()

import tinypico as TinyPICO
import time, random, micropython
from ntptime import settime

# Say hello
print("\nHello from TinyPICO!")
print("--------------------\n")

# Show some info on boot
print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

# Show available memory
print("Memory Info - micropython.mem_info()")
print("------------------------------------")
micropython.mem_info()


def load_config():
    import ujson
    with open('config.json') as f:
        return ujson.loads(f.read())

def do_connect(config):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(config['essid'], config['password'])
        while not sta_if.isconnected():
            pass
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        print('Network config:', sta_if.ifconfig())

config = load_config()
do_connect(config)

import webrepl
webrepl.start()

settime()

from rtttl_player import play_song

from webserver import start_in_thread
start_in_thread()

gc.collect()
