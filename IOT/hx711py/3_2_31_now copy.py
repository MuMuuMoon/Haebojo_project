#! /usr/bin/python2

import time
import sys
import requests

EMULATE_HX711=False

referenceUnit = 1
url="http://192.168.123.2:5555/fromLoadcell"

first1=first2=first3 = 0
before1=before2=before3 =0
now1=now2=now3 =0
changing=i=0

pepsi=150000
YOGU=27000
bola=7400

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

flag = True
errorRange=1000
while True:
    try:
        datas1={
            "price1" : 0
            ,"price2" : 0
            ,"price3" : 0
        }

        while True:
            before1 = round(hx1.get_weight())
            before2 = round(hx2.get_weight())
            before3 = round(hx3.get_weight())
            
            print("before1 = >  " + str(-before1) + "   before2 = >  " + str(-before2) + "  before3 = >  " +str(-before3))
            if((abs(before2)>errorRange) or (abs(before3)>errorRange)):
                print("무게변화감지")
                while True:
                    time.sleep(1)
                    if(flag==False):
                        flag=True
                        print("브레이크되었다")
                        break
                    now1 = round(hx1.get_weight())
                    now2 = round(hx2.get_weight())
                    now3 = round(hx3.get_weight())
                    
                                  
                    
                    
                    if(abs(now2)> 1000 or abs(now3)> 1000):
                        if(abs(now2)> (pepsi-(pepsi*0.5))):
                            print("pepsi 1개 결제")
                            datas1['price2']=1
                        if(abs(now2)> ((pepsi*2)-(pepsi*0.5))):
                            print("pepsi 2개 결제")
                            datas1['price2']=2
                        if(abs(now3)> (YOGU-(YOGU*0.5))):
                            print("YOGU 1개 결제")
                            datas1['price3']=1
                        if(abs(now3)> (bola-(bola*0.5))):
                            print("bola 1개 결제")
                        requests.post(url, data=datas1)
                        while True:
                            time.sleep(1)
                            now1=round(hx1.get_weight())
                            now2=round(hx2.get_weight())
                            now3=round(hx3.get_weight())
                            if(flag==False):
                                print("break되었습니다11")
                                break
                            print("결제취소대기")
                            print("now1 = >  " + str(now1) + "   now2 = >  " + str(now2) + "   now3 = >  " +str(now3))

                            if( abs(before2)-abs(now2) < (pepsi+(pepsi*0.5)) ):
                                print("pepsi 1개 결제취소")
                                hx2.reset()
                                hx3.reset()
                                if(now2>-250):
                                    datas1['price2']=0
                                if(now3>-400):
                                    datas1['price3']=0
                                requests.post(url, data=datas1)
                                time.sleep(1)
                                print("break되었습니다22")
                                flag=False
                                break    

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
