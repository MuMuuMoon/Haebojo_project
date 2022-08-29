#! /usr/bin/python2

import time
import sys
import requests
from multiprocessing import Pool
import multiprocessing as mp

EMULATE_HX711=False

referenceUnit = 1

url="http://192.168.123.2:5555/test"

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx= [HX711(4,17), HX711(18,27), HX711(22,23)]

for i in range(0,3):
    hx[i].set_reading_format("MSB", "MSB")

for i in range(0,3):
    hx[i].set_reference_unit(referenceUnit)
    hx[i].reset()
    hx[i].tare()
print("Tare done! Add weight now...")

# print("No1: ", str(hx[0].get_weight()))
print("No2: ", str(hx[1].get_weight()))
print("No3: ", str(hx[2].get_weight()))