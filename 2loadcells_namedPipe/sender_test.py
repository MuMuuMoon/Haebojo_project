import serial
import time
import os.path

FIFO_FILENAME = './fifo-test'
if not os.path.exists(FIFO_FILENAME):
    os.mkfifo(FIFO_FILENAME)

if os.path.exists(FIFO_FILENAME):
    fp_fifo = open(FIFO_FILENAME, "w")
    data = ''
    fp_fifo.write(data)

    while True:
        fp_fifo.write('a')