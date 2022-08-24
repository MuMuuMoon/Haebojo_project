#! /usr/bin/python2

import time
import sys
import requests

EMULATE_HX711=False

global i, first, before, now

i=0

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

# hx = HX711(17,4)
# hx2= HX711(27,18)
# hx3= HX711(23,22)
# hx4= HX711(10,24)

hx = HX711(4,17)
hx2= HX711(18,27)
hx3= HX711(22,23)
hx4= HX711(24,10)
# (dout, sck) 4,17/ 18,27/ 22,23/ 24,10

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")
hx2.set_reading_format("MSB", "MSB")
hx3.set_reading_format("MSB", "MSB")
hx4.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
hx2.set_reference_unit(referenceUnit)
hx2.reset()
hx2.tare()
hx3.set_reference_unit(referenceUnit)
hx3.reset()
hx3.tare()
hx4.set_reference_unit(referenceUnit)
hx4.reset()
hx4.tare()
print("Tare done! Add weight now...")
# time.sleep(5)

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

# avg=0
# cnt=0
# val3_min=9999999
# val3_max=-9999999


while True:
    try:
        #꼼수
        
        global i
        
        
        
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = round(hx.get_weight(5) * -1)
        val2 = round(hx2.get_weight(5) * -1) 
        val3 = round(hx3.get_weight(5) * -1)
        val4 = round(hx4.get_weight(5) * -1)  
        if(i==0):
            tempval = round(hx.get_weight(5) * -1)
            tempval2 = round(hx2.get_weight(5) * -1) 
            tempval3 = round(hx3.get_weight(5) * -1)
            tempval4 = round(hx4.get_weight(5) * -1)  
        
        if((tempval*2)-val<0 | (tempval2*2)-val2<0 | (tempval3*2)-val3<0 | (tempval4*2)-val4<0):
            response = requests.post(url, data=datas)
            
        
        print(val3_before)      
        datas={
            'val' : val
            ,'val2' : val2
            ,'val3' : val3
            ,'val4' : val4
        }
        # avg+=val3
        # cnt+=1
        # if cnt==10:
        #     avg/=10
        #     print(avg)
        #     break
        print(str(val)+ " , " + str(val2) + " , " +  str(val3)+ " , " + str(val4))
        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        hx2.power_down()
        hx2.power_up()
        hx3.power_down()
        hx3.power_up()
        hx4.power_down()
        hx4.power_up()  
        
        # if(val > 50 | val2> 50 | val3 > 50 | val4 > 50):
        #     response = requests.post(url, data=datas)    
        val3_before=val3  
        
        if abs(val3-val3_before) > val3_max :
            val3_max= abs(val3-val3_before)
        if abs(val3-val3_before) < val3_min :
            val3_min= abs(val3-val3_before)
        print(str(val3_min) + ", " + str(val3_max))
        
        time.sleep(0.1)

        
        i+=1
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
