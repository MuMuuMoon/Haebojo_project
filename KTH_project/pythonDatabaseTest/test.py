import qrcode
from PIL import Image
import time
import sqlite3 as sql
from flask import Flask, render_template

app = Flask(__name__)
global index
index=0

@app.route('/')
def makeqrcode():
    global index
    index += 1
    y = str(index)
    img = qrcode.make("" + y)
    img.save("/home/fhxlvnf/pythonDatabaseTest/static/img/" + y + ".png")

#    image = Image.open("/home/fhxlvnf/pythonDatabaseTest/static/img/" + y + ".png")
#    image.show()

    time.sleep(3)
    return render_template('index.html',image_file="img/"+y+".png",y=y)



if __name__ == '__main__':
    app.run('0.0.0.0', 5001)
