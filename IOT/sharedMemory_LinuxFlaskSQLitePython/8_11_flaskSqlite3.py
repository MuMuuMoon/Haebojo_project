import sqlite3
from flask import Flask, render_template, request, redirect, url_for

DATABASE_NAME = '2loadcells.db'
TABLE_NAME_A = "person"
TABLE_NAME_B = "loadcell"
DATABASE = '/home/fhxlvnf/pythonTest/' + DATABASE_NAME
app = Flask(__name__)


conn = sqlite3.connect(DATABASE_NAME)
print ("Opened database successfully")
conn.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_A + ' (indexPerson int primary key , item TEXT, num TEXT, price TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_B + ' (indexWeight int ,item TEXT, num TEXT, price TEXT, foreign key (indexWeight) references person (indexPerson))')
print ("Table created successfully")
conn.close()



@app.route('/')
def showdata():
    #데이터베이스에서 데이터를 가져 온다.
    con = sqlite3.connect(DATABASE_NAME)
    con.row_factory = sqlite3.Row
    cur1 = con.cursor()
    cur2 = con.cursor()

    cur1.execute("select * from " + TABLE_NAME_A)
    rows1 = cur1.fetchall()

    cur2.execute("select * from " + TABLE_NAME_B)
    rows2 = cur2.fetchall()
    print("DB:")
    print(rows1)
    print(rows2)
    return render_template('showresult.html', rows1 = rows1, rows2 = rows2)

@app.route('/insert', methods = ['POST','GET'])
def insert():
    msg = ""
    if request.method == 'POST':
        try:
            indexPerson = request.form['indexPerson']
            item = request.form['item']
            num = request.form['num']
            price = request.form['price']

            item2 = request.form['item2']
            num2 = request.form['num2']
            price2 = request.form['price2']

            with sqlite3.connect(DATABASE_NAME) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO " + TABLE_NAME_A + " (indexPerson ,item, num, price) VALUES (?, ?, ?, ?)", (indexPerson, item, num, price))
                cur.execute("INSERT INTO " + TABLE_NAME_B + " (indexWeight, item, num, price) VALUES (?, ?, ?, ?)", (indexPerson, item2, num2, price2))
                con.commit()
                msg = "Recod successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally :
            return redirect(url_for("showdata"))
            con.close()

if "__main__"==__name__:
    app.run('localhost',5005)
