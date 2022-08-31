import qrcode
from PIL import Image
import time
import sqlite3 as sql
from flask import Flask, render_template

app = Flask(__name__)
global i
i=0

@app.route('/')
def makeqrcode():
    global i
    i += 1
    y = str(i)
    img = qrcode.make("" + y)
    img.save("/home/kth/Desktop/flask_server/static/img/" + y + ".png")

    image = Image.open("/home/kth/Desktop/flask_server/static/img/" + y + ".png")
#    image.show()

    time.sleep(3)
    return render_template('index.html',image_file="img/"+y+".png",y=y)

    

if __name__ == '__main__':
    app.run('localhost', 5002)
