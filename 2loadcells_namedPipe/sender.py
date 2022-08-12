import serial
import time
import os.path

NodeMCU = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(3)  # 초기화 완료될 시간 약간 기다리기.

FIFO_FILENAME = './fifo-test'
if not os.path.exists(FIFO_FILENAME):
    os.mkfifo(FIFO_FILENAME)

if os.path.exists(FIFO_FILENAME):
    fp_fifo = open(FIFO_FILENAME, "w")
    while True:     
        c = NodeMCU.readline()
        data = c.decode()
        print(data)
        fp_fifo.write(data)
        os.remove(FIFO_FILENAME)
        os.mkfifo(FIFO_FILENAME)        
        time.sleep(0.1)


NodeMCU.close()