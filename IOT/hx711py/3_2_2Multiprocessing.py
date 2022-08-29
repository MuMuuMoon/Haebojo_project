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

def loadcell(num):
    before=[0,0,0]
    now=[0,0,0]
    while True:
        c_proc= mp.current_process()
        print("loadcell num: ",num+1,", PID: ",c_proc.pid)
        before[num] = round(hx[num].get_weight(5))
        if(abs(first[num]-before[num])>400):
            print(num+1, " 무게변화감지때 무게값 : "+ str(before[num]))
            print(num+1," 무게변화감지")
            while True:
                now[num] = round(hx[num].get_weight(5))
                if(abs(before[num]-now[num])<400):
                    print(num+1," 결제감지되었을대 무게값 : " +str(now[num]))
                    print(num+1," 결제감지")
                    requests.post(url, data=datas1)
                    while True:
                        now[num]=round(hx[num].get_weight(5))
                        print(num+1," 결제취소되기전에 무게값 : " + str(now[num]))
                        if(abs(first[num]-now[num])<400):
                            print(num+1," 결제취소")
                            requests.post(url, data=datas1)
                            time.sleep(1)
                            break

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
    first[i] = round(hx[i].get_weight(5))
for i in range(0,3):
    print("초기 물건이 있었을때 first",i+1," 값: " + str(first[i]))

while True:
    try:
        datas1={
            "first" : 0
            ,"second" : 0
            ,"third" : 0
        }
        
        p=Pool(3)
        p.map(loadcell,[0,1,2])
        
        for i in range(0,3):    
            hx[i].power_down()
            hx[i].power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
