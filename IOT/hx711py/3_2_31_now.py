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
        
        print("before1        "+str(before2))
        print("hx1.tare       "+str(hx2.tare()+339000))
        print("\n")
        if(abs(before1+hx1.tare()+125400)>10000 or abs(before2+hx2.tare()+339000)>10000 or abs(before3+hx3.tare()+97100)>10000):
            print("11무게변화감지때 무게값 : "+ str(before1))
            print("22무게변화감지때 무게값 : "+ str(before2))
            print("33무게변화감지때 무게값 : "+ str(before3))
            while True:
               
               
                # print("now1            " +str(now2))
                print("tare            " +str(abs(hx1.tare()+125400)))
                print("tare            " +str(abs(hx2.tare()+339000)))
                print("tare            " +str(abs(hx3.tare()+97100)))
                print("\n")
                # print("before1=>" + str(before1))
                # print("now1=>"+ str(now1))
                if((abs(hx1.tare()+125400)<10000) or (abs(hx2.tare()+339000)<10000) or (abs(hx3.tare()+97100)<10000)):
                    print("2번째while문 11결제감지되었을대 무게값 : " +str(now1))
                    print("2번째while문 22결제감지되었을대 무게값 : " +str(now2))
                    print("2번째while문 33결제감지되었을대 무게값 : " +str(now3))
                    requests.post(url, data=datas1)
                    while True:
                 
                        print("3번째while문 11결제취소되기전에 무게값 : " + str(now1))
                        print("3번째while문 22결제취소되기전에 무게값 : " + str(now2))
                        print("3번째while문 33결제취소되기전에 무게값 : " + str(now3))
                        if((abs(hx1.tare()+125400)<10000) or (abs(hx2.tare()+339000)<10000) or (abs(hx3.tare()+97100)<10000)):
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
flag = True
while True:
    try:
        datas1={
            "first" : -1
        }
        datas2={
            "first" : -1
        }
        temp=750
        while True:
            before1 = round(hx1.get_weight(7))
            before2 = round(hx2.get_weight(7))
            before3 = round(hx3.get_weight(7))
            
            print("first1-before1 = >  " + str(first1-before1) + "   first2-before2 = >  " + str(first2-before2) + "  first3-before3 = >  " +str(first3-before3))
            if((abs(first2-before2)>400) or (abs(first3-before3)>400)):
                print("무게변화감지때 무게값 : "+ str(before1))
                print("무게변화감지때 무게값 : "+ str(before2))
                print("무게변화감지때 무게값 : "+ str(before3))
                print("무게변화감지")
                # print("무게변화감지first" + str(first))
                # print("무게변화감지before"+str(before))
                while True:
                    if(flag==False):
                        flag=True
                        print("브레이크되었다")
                        break
                    # hx1.tare()
                    # hx2.tare()
                    # hx3.tare()
                    #무게가 가벼워지면 이전값에서 현재값을 뺀 것이 400보다 커진다
                    now1 = round(hx1.get_weight(7))
                    now2 = round(hx2.get_weight(7))
                    now3 = round(hx3.get_weight(7))
                    # print("before1-now1        " +str(before1-now1))
                    # print("before1-now1 = >    " + str(before1-now1) +   "   before2-now2 = >    " + str(before2-now2) +   "   before3-now3 = >  " +str(before3-now3))
                    # print("first1-before1 = >  " + str(first1-before1) + "   first2-before2 = >  " + str(first2-before2) + "   first3-before3 = >  " +str(first3-before3))
                    # print("now2 = >            " + str(now2)+            "   now3 = >            "+str(now3))
                    # print("before2 = >            " + str(before2)+            "   before3 = >            "+str(before3))
                    # print("tare2=>              " + str(hx2.tare())+"  tare3=>              "+str(hx3.tare()))
                    # print("get_weight3=>           " + str(hx3.get_weight(7))+"  get_weight3=>              "+str(hx3.get_weight(7)))
                    # print("\n")
                    # print("합계 : 2=> " +str(hx2.tare()-before2) + "   합계 : 3=> " +str(hx3.tare()-before3))
                    # print("\n")
                    if((((now2)<-10) or ((now3)<-10))):
                        #결제감지가됐을때는 마이너스가된다 now값이
                        print("결제감지되었을대 무게값 : " +str(now1))
                        print("결제감지되었을대 무게값 : " +str(now2))
                        print("결제감지되었을대 무게값 : " +str(now3))
                        print("결제감지")
                        requests.post(url, data=datas1)
                        while True:
                            
                            now1=round(hx1.get_weight(7))
                            now2=round(hx2.get_weight(7))
                            now3=round(hx3.get_weight(7))
                            if(flag==False):
                                print("break되었습니다11")
                                
                                break
                            print("결제취소되기전에 무게값 : " + str(now1))
                            print("결제취소되기전에 무게값 : " + str(now2))
                            print("결제취소되기전에 무게값 : " + str(now3))
                            print("now1 = >  " + str(now1) + "   now2 = >  " + str(now2) + "   now3 = >  " +str(now3))

                            if(((now2)>0) and ((now3)>0)):
                                print("결제취소")
                                hx2.reset()
                                hx3.reset()
                                requests.post(url, data=datas1)
                                # print("결제취소first" + str(first))
                                # print("결제취소now"+str(now))
                                time.sleep(1)
                                print("break되었습니다22")
                                flag=False
                                break    
        
        # loadcell(first1,first2,first3)
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
