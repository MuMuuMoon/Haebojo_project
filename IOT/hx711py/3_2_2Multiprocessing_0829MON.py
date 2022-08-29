#! /usr/bin/python2

import time
import sys
import requests
from multiprocessing import Pool
import multiprocessing as mp

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
        before[num] = round(hx[num].get_weight())
        weightDiff= abs( abs(first[num]) - abs(before[num]) )
        print(num+1, ": ", before[num])
        
        if( abs(before[num]) >errorRange): # 무게 변화 감지.                                   
            while True:
                now[num] = round(hx[num].get_weight())  
                print(num+1, ": ", now[num])              
                # if(abs( abs(before[num]) - abs(now[num])) < errorRange): # 결제 감지.
                #     print(num+1," 결제감지 후 무게값 : " +str(now[num]))
                    
                #     if(num+1==2):
                #         temp= int(abs(now)/pepsi80)
                #         print("pepsi ", temp , "개 결제감지")
                #         num["pepsi"]-= temp
                #     if( num+1==3 and (bola80< abs(now)) and (abs(now) <YOGU120) ):
                #         temp=int(abs(now)/YOGU80)
                #         print("YOGU ", temp , "개 결제감지")
                #         num["YOGU"]-= temp
                #     if(num+1==3 and abs(now) < bola120):
                #         temp=int(abs(now)/bola80)
                #         print("bola ", temp, "개 결제감지") 
                #         num["bola"]-= temp                    
                #     # requests.post(url, data=datas1) # 결제 정보 전송.
                #     print(num)
                    
                    # while True:
                    #     now[num]=round(hx[num].get_weight())
                    #     # if(num+1)
                    #     weightDiff= abs( abs(before[num]) - abs(now[num]) )
                    #     print(num+1," 결제취소되기전에 무게값 : " + str(now[num]))
                    #     if(num+1==2 and pepsi90 < weightDiff and weightDiff < pepsi110*2): # 결제 취소 감지.
                    #         print("pepsi 1개 결제취소감지")
                    #         datas1['pepsi']-=1                
                    #     if(num+1==2 and pepsi < weightDiff < pepsi*2):
                    #         print("pepsi 2개 결제취소감지")
                    #         datas1['pepsi']-=2                
                    #     if(num+1==3 and weightDiff < YOGU):
                    #         print("YOGU 1개 결제취소감지")
                    #         datas1['YOGU']-=1                
                    #     if(num+1==3 and weightDiff < bola):
                    #         print("bola 1개 결제취소감지") 
                    #         datas1['bola']-=1        
                                        
                    #     if(weightDiff < errorRange): 
                    #         print(num+1," 결제취소")
                    #         # requests.post(url, data=datas1)
                    #         print(datas1)
                    #         time.sleep(1)
                    #         break

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
        datas1={
            "pepsi" : 0,
            "YOGU" : 0,
            "bola" : 0
        }
        num={
            "pepsi" : 2,
            "YOGU" : 1,
            "bola" : 1
        }
        
        p=Pool(2)
        p.map(loadcell,[1])
        
        for i in range(1,3):    
            hx[i].power_down()
            hx[i].power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
