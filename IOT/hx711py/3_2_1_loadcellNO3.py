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
print("초기 물건이 있었을때 first값 : " + str(first))
while True:
    try:
        datas={
            "first" : -1
        }
        datas2={
            "first" : -1
        }
        while True:
            before = round(hx3.get_weight(5))
            print("first-before = >  " + str(first-before))
            
            if(abs(first-before)>400):
                print("무게변화감지때 무게값 : "+ str(before))
                print("무게변화감지")
                # print("무게변화감지first" + str(first))
                # print("무게변화감지before"+str(before))
                while True:
                    now = round(hx3.get_weight(5))
                    print("before-now = >  " + str(before-now))
                    if(abs(before-now)<400):
                        print("결제감지되었을대 무게값 : " +str(now))
                        print("결제감지")
                        requests.post(url, data=datas)
                        while True:
                            now=round(hx3.get_weight(5))
                            print("결제취소되기전에 무게값 : " + str(now))
                            print("first-now = >  " + str(first-now))
                            if(abs(first-now)<400):
                                print("결제취소")
                                requests.post(url, data=datas2)
                                # print("결제취소first" + str(first))
                                # print("결제취소now"+str(now))
                                time.sleep(10)
                                break            
        hx3.power_down()
        hx3.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
