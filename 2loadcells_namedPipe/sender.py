import serial
import time
import os.path

# NodeMCU=serial.Serial(port="/dev/ttyACM0", baudrate=115200)
NodeMCU = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(3)  # 초기화 완료될 시간 약간 기다리기.

FIFO_FILENAME = './fifo-test'
if not os.path.exists(FIFO_FILENAME):
    os.mkfifo(FIFO_FILENAME)

if os.path.exists(FIFO_FILENAME):
    fp_fifo = open(FIFO_FILENAME, "w")
    data = ''
    fp_fifo.write(data)

    while True:
        c = NodeMCU.readline()
        data = c.decode()
        fp_fifo.write(data)

# s = '0, 0'
# print(s)

# while(1):
#     c = NodeMCU.readline()  # enter 전까지 읽어오기.
#     s = c.decode()
#     print(s)
