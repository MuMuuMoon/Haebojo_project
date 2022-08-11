import os.path

FIFO_FILENAME = './fifo-test'

if os.path.exists(FIFO_FILENAME):
    fp_fifo = open(FIFO_FILENAME, "r")
    i = 0
    while True:
        with open(FIFO_FILENAME, 'r') as fifo:
            data = fifo.read()
            line = data.split('\n') # 없애고 바로 print(data)하면 시리얼모니터에서 보이는 모습 그대로 출력 됨.
            for str in line:
                i = i+1
                print(str + "%4d" % i)