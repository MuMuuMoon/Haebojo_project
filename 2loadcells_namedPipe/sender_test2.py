import serial
import time

NodeMCU = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(3)

while True: 
    print(repr(NodeMCU.readline()))