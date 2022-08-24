#! /usr/bin/python2

import time
import sys
import requests

EMULATE_HX711=False

referenceUnit = 1
url="http://192.168.123.3:5555/test"

first1 = 0
first2 = 0
first3 = 0
before1 =0
before2 =0
before3 =0
now1 =0
now2 =0
now3 =0
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

def loadcell(first1,first2,first3):
    while True:
        before1 = round(hx1.get_weight(5))
        before2 = round(hx2.get_weight(5))
        before3 = round(hx3.get_weight(5))
        if(abs(first1-before1)>2800 | abs(first2-before2)>800 | abs(first3-before3)>2800):
            print("11무게변화감지때 무게값 : "+ str(before1))
            print("22무게변화감지때 무게값 : "+ str(before2))
            print("33무게변화감지때 무게값 : "+ str(before3))
            while True:
               
                now1 = round(hx1.get_weight(5))
                now2 = round(hx2.get_weight(5))
                now3 = round(hx3.get_weight(5))
                print("before1=>" + str(before1))
                print("now1=>"+ str(now1))
                if((abs(before1-now1)<2800) | (abs(before2-now2)<800) | (abs(before3-now3)<2800)):
                    print("11결제감지되었을대 무게값 : " +str(now1))
                    print("22결제감지되었을대 무게값 : " +str(now2))
                    print("33결제감지되었을대 무게값 : " +str(now3))
                    requests.post(url, data=datas1)
                    while True:
                        now1=round(hx1.get_weight(5))
                        now2=round(hx2.get_weight(5))
                        now3=round(hx3.get_weight(5))
                        print("11결제취소되기전에 무게값 : " + str(now1))
                        print("22결제취소되기전에 무게값 : " + str(now2))
                        print("33결제취소되기전에 무게값 : " + str(now3))
                        if((abs(first1-now1)<2800) | (abs(first2-now2)<800) | (abs(first3-now3)<2800)):
                            print("결제취소")
                            requests.post(url, data=datas1)
                            time.sleep(1)
                            break



hx1 = HX711(4,17)
hx2= HX711(18,27)
hx3= HX711(22,23)
# (dout, sck) 4,17/ 18,27/ 22,23/ 24,10

hx1.set_reading_format("MSB", "MSB")
hx2.set_reading_format("MSB", "MSB")
hx3.set_reading_format("MSB", "MSB")

hx1.set_reference_unit(referenceUnit)
hx1.reset()
hx1.tare()
hx2.set_reference_unit(referenceUnit)
hx2.reset()
hx2.tare()
hx3.set_reference_unit(referenceUnit)
hx3.reset()
hx3.tare()
print("Tare done! Add weight now...")

first1 = round(hx1.get_weight(5))
first2 = round(hx2.get_weight(5))
first3 = round(hx3.get_weight(5))

print("초기 물건이 있었을때 first값 : " + str(first1))
print("초기 물건이 있었을때 first2값 : " + str(first2))
print("초기 물건이 있었을때 first3값 : " + str(first3))
while True:
    try:
        datas1={
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
        
        loadcell(first1,first2,first3)
        # loadcell2(first2)
        # loadcell3(first3)
    
        
            
        hx1.power_down()
        hx1.power_up()
        hx2.power_down()
        hx2.power_up()
        hx3.power_down()
        hx3.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
