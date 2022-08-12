import serial
import time
import os.path

# NodeMCU=serial.Serial(port="/dev/ttyACM0", baudrate=115200)
NodeMCU = serial.Serial('/dev/ttyACM0', 9600,timeout=10)
time.sleep(3)  # 초기화 완료될 시간 약간 기다리기.

FIFO_FILENAME = './fifo-test'
if not os.path.exists(FIFO_FILENAME):
    os.mkfifo(FIFO_FILENAME)

if os.path.exists(FIFO_FILENAME):
    fp_fifo = open(FIFO_FILENAME, "w")
    data = ''
    fp_fifo.write(data)
    c = NodeMCU.readlines()
    data = c.decode()
    fp_fifo.write(data)
    NodeMCU.close()