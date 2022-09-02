#! /usr/bin/python2

import time
import sys
import requests

EMULATE_HX711=False

pepsi=150000
pepsi80=pepsi*0.8
pepsi120=pepsi*1.2
YOGU=27000
YOGU80=YOGU*0.8
YOGU120=YOGU*1.2
bola=7400
bola80=bola*0.8
bola120=bola*1.2

errorRange=1000
referenceUnit = 1

url="http://192.168.123.7:5555/fromLoadcell"

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

first=[0,0,0]
for i in range(0,3):
    first[i] = round(hx[i].get_weight())
for i in range(0,3):
    print("초기 물건이 있었을때 first",i+1," 값: " + str(first[i]))

while True:
    try:
        stock={
            "YOGU" : 1,
            "pepsi" : 2,
            "bola" : 1
        }
        num={
            "YOGU" : 0,
            "pepsi" : 0,
            "bola" : 0
        }
        
        while True:
            # 로드셀 3개 실시간 갯수 업데이트.
            num["YOGU"] = int(abs(round(hx[0].get_weight())) / YOGU80)
            num["pepsi"] = int(abs(round(hx[1].get_weight())) / pepsi80)
            num["bola"] = int(abs(round(hx[2].get_weight())) / bola80)
            print(num)
            
            requests.post(url, data=num) # 서버로 결제 정보 전송.

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
