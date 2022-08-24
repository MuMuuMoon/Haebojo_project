#! /usr/bin/python2

import time
import sys
import requests

EMULATE_HX711=False

referenceUnit = 1
url="http://192.168.123.3:5555/test"


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

while True:
    try:
        if cnt>0:
            val3_before=val3
        cnt+=1
        # if cnt==500:
        #     break
        
        val3 = round(hx3.get_weight(5)) 
        print("val3 : " + str(val3))
        
        if abs(val3-val3_before) > val3_max :
            val3_max= abs(val3-val3_before)
        if abs(val3-val3_before) < val3_min :
            val3_min= abs(val3-val3_before)
        print("min: " + str(val3_min) + ", max: " + str(val3_max))    
        
        if abs(val3-val3_before) >= 200 : # 물건 집음. 
            before_detection= val3_before
            while True:
                val3 = round(hx3.get_weight(5))
                if (stableCheck()== 1): # 변화가 없는 상태.
                    if (stable >= 5) & (abs(before_detection-val3)<= 200): # 물건 집었다 다시 놓은 경우.
                        break    
                    if (stable >= 5) & (abs(before_detection-val3)>= 200): # 결제 예정.
                        datas={
                            'val3' : -1
                        }
                        response = requests.post(url, data=datas)
                        print("결제예정------------------------------------------")
                        break
                else:
                    break
                val3_before=val3
        
        hx3.power_down()
        hx3.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
