import sqlite3
from flask import Flask, render_template, request, redirect, url_for

#리눅스에서 사용중인 계정이름
#linux_account_name = "fhxlvnf"
#db이름 이값만바꾸면 새로운 환경이된다
DATABASE_NAME = 'database76.db'
#테이블이름
TABLE_NAME_A = "loadcell"
TABLE_NAME_B = "person"
#절대경로
#DATABASE = '/home/' + linux_account_name +
# '/pythonDatabaseTest/' + DATABASE_NAME

global qrdatalist
global qrdata
global qrFlag
global opencvFlag
global opencvFlagFirstIn
global loadcellWeight
global qrdataindex

qrdatalist=[]
opencvFlag = False
qrFlag = False
opencvFlagFirstIn = False
qrdataindex=-1

loadcellPrice1 = 200
loadcellPrice2 = 1300
loadcellPrice3 = 500


app = Flask(__name__)


conn = sqlite3.connect(DATABASE_NAME)
print("Opened database successfully")
conn.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_A + ' (indexPerson int primary key , item TEXT, num TEXT, price TEXT, opencvlabel TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_B + ' (indexWeight int ,item TEXT, num TEXT, price TEXT, foreign key (indexWeight) references person (indexPerson))')
print("Table created successfully")
conn.close()

#서버로 구현해서 각 파트에서 받은 data를 정리해서 웹페이지에 보여주는것

#[0,0,0]

#로드셀에 좌표정보는 이미 정해져있는 상수 데이터
#opencv에서 받아온 데이터 xy가 로드셀에 대한 좌표정보 xy와 겹치고 로드셀무게정보가 변하게되면 해당 qrdata의 인덱스를 알아내어 로드셀db정보 업데이트

#qrdatalist에 있는 리스트에 값이 들어있는 순서대로 opencv에서 제일처음라벨링된 객체와 맵핑하게 된다
#이해를 돕는 ex) 만약 최초에 qr인증을 한 사람이 35번을 찍고 들어온 상태에서 opencv에서 라벨링을 1번으로 하게된다면
#35번이라는 qr코드값 과 라벨링된 숫자인 1번은 서로 연관관계 라는 것

#아두이노에서 메세지를 보내는건 오로지 무게변화 감지할때만이라는 가정하에
#아두이노에서 무게가 변화한 것을 감지하면 그 순간 fromLoadcell에 메소드
#(이때 그 메소드라는것은 opencv에 x,y좌표값을 글로벌 변수에 저장하는 코드가 들어있다)
#를 call 해주고 return에 redirect를 이용해서 @app.route('')아래에 특정 메소드를 호출한다
#리다이렉트로 호출된 메소드안에서는 update문을 이용하여


#추후데이터가 서버로 전송될때
#받는코드 ==> " request.get_data() "
#이것을 리스트화시켜서 각각 item, num, price에 대입시키는 코드로 치환하면 html입력폼없이 동작하게 된다
#index라는 변수는 제일 처음에 사람이 입장할때 찍은 qr코드 문자열이 저장되어있는 변수로써
#개인별 작업을 마친뒤 실제 취합하는 과정에서 로드셀에 무게가 변했을때
#물건을 집은 고객의 qr데이터의 정보를 담고있어야하는 변수이다


@app.route('/')
def index():
    return render_template("temp.html")

@app.route('/test', methods = ['GET','POST'])
def test():
    if (request.method == 'POST'):
        listval=[]
        loadcelldata = str(request.get_data())[2:-1]
        loadcelldatalist=loadcelldata.split("&")
        for i in loadcelldatalist:
            listval.append(i.split("=")[1])
        print(listval[0])
        print(listval[1])
        print("=======>" + str(loadcelldata))



    return render_template("temp.html")

@app.route('/fromQR', methods=['POST'])
def handle_QR():
    if (request.method == 'POST'):
        #생으로 넘어온 qr코드정보를 숫자만 잘라내야 하기 때문에 str로 감싼뒤 슬라이싱
        #이후에 다시 db에 넣을때 db타입이 int이므로 int로 다시 형변환
        global qrdata
        global qrFlag
        global opencvFlagFirstIn
        global qrdataindex
        qrFlag = False
        #이 플래그는 만약 사람이 입장하였을때 opencv로부터 데이터를 받아들여서 매핑하는것을 활성화시키기위해 True로 설정
        opencvFlagFirstIn = True
        qrdata = int(str(request.get_data())[2:-1])
        qrdatalist.append(qrdata)
        #어떤식으로든지 데이터를 보내주시면 그것을 제가 여기서 알맞게 가공해서 디비에 넣습니다
        #되는지 확인해야 하니까 저도 DB table?이 있어야 한다.
        #123, 123, 324
        print("qrtata=>   " +str(qrdata))
        print(qrdatalist)

        try:

            qrdataindex+=1

            indexPerson = qrdata
            item = None
            num = None
            price = None
            opencvlabel = None
            item2 = None
            num2 = None
            price2 = None


            with sqlite3.connect(DATABASE_NAME) as con:
                cur = con.cursor()
                #디비에 실질적을 들어가는 코드
                cur.execute("INSERT INTO " + TABLE_NAME_A + " (indexPerson ,item, num, price, opencvlabel) VALUES (?, ?, ?, ?, ?)", (indexPerson, item, num, price, opencvlabel))
                cur.execute("INSERT INTO " + TABLE_NAME_B + " (indexWeight, item, num, price) VALUES (?, ?, ?, ?)", (indexPerson, item2, num2, price2))
                con.commit()
        except:
            con.rollback()
        finally :
            con.close()
            qrFlag = True
            return redirect(url_for("showdata"))


@app.route('/fromLoadcell', methods = ['GET','POST'])
def handle_loadcell():
    global opencvFlag
    if (request.method == 'POST'):
        #갑자기 opencvFlag를 True로 한 까닭은 로드셀 정보가 왔을때만 opencv에 위치정보를 받겠다는 뜻
        opencvFlag = True
        listval = []

        loadcelldata = str(request.get_data())[2:-1]
        loadcelldatalist = loadcelldata.split("&")
        for i in loadcelldatalist:
            listval.append(i.split("=")[1])
        # print(listval[0])
        # print(listval[1])
        # print(listval[2])
        try:

            index = 1

            item = int(listval[0]) * loadcellPrice1
            num = int(listval[1]) * loadcellPrice2
            price = int(listval[2]) * loadcellPrice3


            opencvlabel = 321



            with sqlite3.connect(DATABASE_NAME) as con:
                cur = con.cursor()
                cur.execute("UPDATE '" + TABLE_NAME_A + "' SET item=?, num=?, price=?, opencvlabel=? WHERE indexPerson=?",(item,num,price,opencvlabel,opencvlabel,index))
                con.commit()
        except:
            con.rollback()
        finally:
            con.close()
            return redirect(url_for("showdata"))


@app.route('/fromOpencv', methods = ['GET','POST'])
def handle_opencv():
    global opencvFlag
    global opencvFlagFirstIn
    global qrdata
    global qrdataindex
    countopencvlength=0
    listvalopencv=[]
    listforpersoncount=[]
    listval=[]

    if (request.method == 'POST'):

        #이부분은 실제 연결시켜서 테스트할때 사용한다(아래 약 12줄)
        # opencvdata = str(request.get_data())[2:-1]
        # listval = opencvdata.split("p&")
        #
        # for i in listval:
        #     listvalopencv.append([x.split("=")[1] for x in i.split("&")])
        # listvalopencv.pop(-1)
        # listforpersoncount = [int(i[0]) for i in listvalopencv]
        #
        # print(opencvdata)
        # print(listval)
        # print(listvalopencv)
        # print(listforpersoncount)

        opencvdata1 = "1=1&1=338&1=125p&2=2&2=87&2=301p&0=3"
        opencvdata2 = "1=1&1=307&1=114p&2=2&2=82&2=301p&3=11&3=0&3=285p&0=4"
        opencvdata3 = "1=1&1=307&1=114p&2=2&2=82&2=301p&3=11&3=0&3=285p&4=24&4=150&4=410p&0=5"
        opencvdata4 = "1=5&1=307&1=114p&2=7&2=82&2=301p&3=11&3=0&3=285p&4=24&4=150&4=410p&5=25&5=150&5=245p&0=6"

        listval = opencvdata4.split("p&")
        for i in listval:
            listvalopencv.append([x.split("=")[1] for x in i.split("&")])
        listvalopencv.pop(-1)
        listforpersoncount = [int(i[0]) for i in listvalopencv]

        print(opencvdata1)
        print(listval)
        print(listvalopencv)
        print(listforpersoncount)
        print(listvalopencv[qrdataindex][0])
        print("qrdata=>"+str(qrdata))

        if(opencvFlagFirstIn==True):
            try:


                item = listvalopencv[qrdataindex][0]
                num = listvalopencv[qrdataindex][1]
                price = listvalopencv[qrdataindex][2]
                opencvlabel = listvalopencv[qrdataindex][0]
                index = qrdata
                with sqlite3.connect(DATABASE_NAME) as con:
                    cur = con.cursor()
                    cur.execute("UPDATE '" + TABLE_NAME_A + "' SET item=?, num=?, price=?, opencvlabel=? WHERE indexPerson=?",(item, num, price, opencvlabel, index))
                    con.commit()
            except:
                con.rollback()
            finally:
                opencvFlagFirstIn = False
                con.close()
                return "123"
    return "123"


        #opencv에서 라벨링중인 객체의 실시간 개체숫자
        # countopencvlength = int(listval[-1].split("=")[1])-1
        #
        # # for i in listval:
        # #     listvalopencv.append(i.split("=")[1])
        # #
        # # #제일 마지막 인덱스를 제거하는 이유는 객체의 개채수를 의미하는 값이기때문에
        # # #애초에 데이터를 넘길때 마지막 인덱스에 개체의 숫자를 넘겼기때문 핸들링시에는 0번만빼면 나머지는 전부 사람의 라벨링아이디 x좌표 y좌표순으로 들어감
        # # listvalopencv.pop(-1)
        # #
        # # print(opencvdata)
        # # print(countopencvlength)
        # # print(listvalopencv)

        # for i in range(0, int(listvalopencv[0])):
        #     print(i)

            # listvalopencv.append([opencvdata[i] for i in opencvdata])
        # print(listvalopencv)
        # return "123"


        # if (opencvFlag == True):
        #     try:
        #         index = 1
        #         item2 = int(listvalopencv[0])
        #         num2 = int(listvalopencv[1])
        #         price2 = int(listvalopencv[2])
        #         opencvlabel = 123
        #
        #
        #         # index = request.form['index']
        #         # item2 = request.form['item2']
        #         # num2 = request.form['num2']
        #         # price2 = request.form['price2']
        #         with sqlite3.connect(DATABASE_NAME) as con:
        #             cur = con.cursor()
        #             cur.execute("UPDATE '" + TABLE_NAME_A + "' SET item=?, num=?, price=? opencvlabel=? WHERE indexPerson=?",(item2, num2, price2, opencvlabel, index))
        #             con.commit()
        #     except:
        #         con.rollback()
        #     finally:
        #         opencvFlag = False
        #         con.close()
        #         return redirect(url_for("showdata"))
        # else:
        #     return "현재는 opencv로부터 데이터 읽기 닫힘 상태"



@app.route('/showlist',methods = ['GET','POST'])
def showdata():
    #if(qrFlag == True):
        #print("qrdata=>"+ str(qrdata))
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

@app.route('/out' ,methods=['GET','POST'])
def outStore():
    if(request.method=='POST'):
        index = request.form['index']

        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cur = con.cursor()
                cur.execute("DELETE FROM " + TABLE_NAME_A + " WHERE indexPerson = (?)",(index))
                cur.execute("DELETE FROM " + TABLE_NAME_B + " WHERE indexWeight = (?)",(index))
                con.commit()
        except:
            con.rollback()
        finally:
            con.close()
            return redirect(url_for("showdata"))
'''
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
            con.close()
            return redirect(url_for("showdata"))
'''

if "__main__"==__name__:
    app.run('0.0.0.0',5555)