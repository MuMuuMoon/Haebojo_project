#! /usr/bin/python2

import time
import sys
import requests

EMULATE_HX711=False

referenceUnit = 1
url="http://192.168.123.3:5555/test"

first = 0
before =0
now =0
changing=0

i=0


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
    
def stableCheck():
    second= round(hx3.get_weight(5))
    for i in range(0,5):
        first= round(hx3.get_weight(5))
        if abs(first-second)<= 200:
            return 1

hx3= HX711(22,23)
# (dout, sck) 4,17/ 18,27/ 22,23/ 24,10

hx3.set_reading_format("MSB", "MSB")

hx3.set_reference_unit(referenceUnit)
hx3.reset()
hx3.tare()
print("Tare done! Add weight now...")

avg=0
cnt=0
val3_min=9999999
val3_max=-9999999
val3_before=0


first = round(hx3.get_weight(5)) #100

while True:
    try:
        
        
        changing = round(hx3.get_weight(5))
        if(abs(first-changing)>200): #200 => first : 100  / changing 0 / before 0
            print("무게변화감지됨")
            before = changing
            
        if(abs(before-changing)<200): # now 0
            print("결제감지됨")
            now = changing
        
        if(abs(now-first)<200): #0 100 < 200 
            print("결제취소됨")
            
        
        datas={
            "first" : first,
            "before" : before,
            "now" : now  
        }
        requests.post(url, data=datas)
            
        hx3.power_down()
        hx3.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
