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

def loadcell(first):
    while True:
        before = round(hx.get_weight(5))
        if(abs(first-before)>400):
            print("11무게변화감지때 무게값 : "+ str(before))
            print("11무게변화감지")
            while True:
                now = round(hx.get_weight(5))
                if(abs(before-now)<400):
                    print("11결제감지되었을대 무게값 : " +str(now))
                    print("11결제감지")
                    requests.post(url, data=datas)
                    while True:
                        now=round(hx.get_weight(5))
                        print("11결제취소되기전에 무게값 : " + str(now))
                        if(abs(first-now)<400):
                            print("11결제취소")
                            requests.post(url, data=datas)
                            time.sleep(1)
                            break


def loadcell2(first2):
    while True:
        before2 = round(hx2.get_weight(5))
        if(abs(first2-before2)>400):
            print("22무게변화감지때 무게값 : "+ str(before2))
            print("22무게변화감지")
            while True:
                now2 = round(hx2.get_weight(5))
                if(abs(before2-now2)<400):
                    print("22결제감지되었을대 무게값 : " +str(now2))
                    print("22결제감지")
                    requests.post(url, data=datas2)
                    while True:
                        now2=round(hx2.get_weight(5))
                        print("22결제취소되기전에 무게값 : " + str(now2))
                        if(abs(first2-now2)<400):
                            print("22결제취소")
                            requests.post(url, data=datas2)
                            time.sleep(1)
                            break

def loadcell3(first3):
    while True:
        before3 = round(hx3.get_weight(5))
        if(abs(first3-before3)>400):
            print("33무게변화감지때 무게값 : "+ str(before3))
            print("33무게변화감지")
            while True:
                now3 = round(hx3.get_weight(5))
                if(abs(before3-now3)<400):
                    print("33결제감지되었을대 무게값 : " +str(now3))
                    print("33결제감지")
                    requests.post(url, data=datas3)
                    while True:
                        now3=round(hx3.get_weight(5))
                        print("33결제취소되기전에 무게값 : " + str(now3))
                        if(abs(first3-now3)<400):
                            print("33결제취소")
                            requests.post(url, data=datas3)
                            time.sleep(1)
                            break

hx = HX711(4,17)
hx2= HX711(18,27)
hx3= HX711(22,23)
# (dout, sck) 4,17/ 18,27/ 22,23/ 24,10

hx.set_reading_format("MSB", "MSB")
hx2.set_reading_format("MSB", "MSB")
hx3.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
hx2.set_reference_unit(referenceUnit)
hx2.reset()
hx2.tare()
hx3.set_reference_unit(referenceUnit)
hx3.reset()
hx3.tare()
print("Tare done! Add weight now...")

first = round(hx.get_weight(5))
first2 = round(hx2.get_weight(5))
first3 = round(hx3.get_weight(5))

print("초기 물건이 있었을때 first값 : " + str(first))
print("초기 물건이 있었을때 first2값 : " + str(first2))
print("초기 물건이 있었을때 first3값 : " + str(first3))
while True:
    try:
        datas={
            "first" : 0
            ,"second" : 0
            ,"third" : 0
        }
        datas2={
            "first" : 0
            ,"second" : 0
            ,"third" : 0
        }
        datas3={
            "first" : 0
            ,"second" : 0
            ,"third" : 0
        }
        
        # loadcell(first)
        # loadcell2(first2)
        loadcell3(first3)
    
        
            
        hx.power_down()
        hx.power_up()
        hx2.power_down()
        hx2.power_up()
        hx3.power_down()
        hx3.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
