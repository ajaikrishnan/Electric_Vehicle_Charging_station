# main.py
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
import mysql.connector
import hashlib
import datetime
from datetime import date
import time
from random import seed
from random import randint
from PIL import Image
import stepic
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="electric_vehicle"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ev_register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ev_station WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login2.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ev_register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        address=request.form['address']
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        account=request.form['account']
        card=request.form['card']
        bank=request.form['bank']
        uname=request.form['uname']
        pass1=request.form['pass']

        cursor = mydb.cursor()
        sql = "INSERT INTO ev_register(id,name,address,mobile,email,account,card,bank,amount,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        val = (maxid,name,address,mobile,email,account,card,bank,'10000',uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="sucess"
        return redirect(url_for('login'))

    return render_template('register.html',msg=msg)

@app.route('/reg_station', methods=['GET', 'POST'])
def reg_station():
    msg=""
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ev_station")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        stype=request.form['stype']
        name=request.form['name']
        area=request.form['area']
        city=request.form['city']
        lat=request.form['lat']
        lon=request.form['lon']
        uname=request.form['uname']
        pass1=request.form['pass']

        cursor = mydb.cursor()
        sql = "INSERT INTO ev_station(id,name,stype,num_charger,area,city,lat,lon,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        val = (maxid,name,stype,'10',area,city,lat,lon,uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="sucess"
        return redirect(url_for('login2'))

    return render_template('reg_station.html',msg=msg)

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    data= cursor.fetchone()
    return render_template('userhome.html',msg=msg, data=data, uname=uname)

@app.route('/station', methods=['GET', 'POST'])
def station():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station")
    data= cursor.fetchall()
    return render_template('station.html',msg=msg, data=data, uname=uname)

@app.route('/slot', methods=['GET', 'POST'])
def slot():
    msg=""
    act=""
    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0
    s7=0
    s8=0
    s9=0
    s10=0
    if 'username' in session:
        uname = session['username']
    #if request.method=='GET':
    sid=request.args.get('sid')
        
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where id=%s",(sid, ))
    dd= cursor.fetchone()
    station=dd[1]
    cursor.execute("SELECT * FROM ev_booking where station=%s and status=1",(sid, ))
    data= cursor.fetchall()

    for nn in data:
        if nn[5]==1:
            s1=1
        if nn[5]==2:
            s2=2
        if nn[5]==3:
            s3=3
        if nn[5]==4:
            s4=4
        if nn[5]==5:
            s5=5
        if nn[5]==6:
            s6=6
        if nn[5]==7:
            s7=7
        if nn[5]==8:
            s8=8
        if nn[5]==9:
            s9=9
        if nn[5]==10:
            s10=10
        
        
    
    act="ok"
    return render_template('slot.html',msg=msg,uname=uname,sid=sid,station=station,act=act,data=data,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10)


@app.route('/select', methods=['GET', 'POST'])
def select():
    if 'username' in session:
        uname = session['username']
    sid=request.args.get('sid')
    rid=request.args.get('rid')
    if request.method=='POST':
        plan=request.form['plan']
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set plan=%s,charge_st=1,charge_min=0,charge_sec=0 where id=%s",(plan, rid))
        mydb.commit()
        return redirect(url_for('slot',sid=sid))
        
    return render_template('select.html',sid=sid,rid=rid)


@app.route('/book', methods=['GET', 'POST'])
def book():
    msg=""
    act=""
    cimage=""
    if 'username' in session:
        uname = session['username']
    sid=request.args.get('sid')
    slot=request.args.get('slot')
        
    #if request.method=='GET':
        #sid=request.args.get('sid')
        #slot=request.args.get('slot')
        
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where id=%s",(sid, ))
    dd= cursor.fetchone()
    station=dd[1]

    #cursor.execute("SELECT * FROM ev_booking where station=%s and status=1",(sid, ))
    #data= cursor.fetchall()
    
    if request.method=='POST':
        carno=request.form['carno']
        reserve=request.form['reserve']
        sid=request.form['sid']
        slot=request.form['slot']
        

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM ev_booking")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        t = time.localtime()
        rtime = time.strftime("%H:%M:%S", t)
        today= date.today()
        rdate= today.strftime("%d-%m-%Y")

        rn=randint(1, 10)
        #if reserve=="1":
        #    cimage="c"+str(rn)+".jpg"
        #else:
        cimage="evch.jpg"
        cursor = mydb.cursor()
        sql = "INSERT INTO ev_booking(id,uname,station,carno,reserve,slot,cimage,rtime,rdate,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        val = (maxid,uname,sid,carno,reserve,slot,cimage,rtime,rdate,'1')
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Booked Success")
        return redirect(url_for('slot',sid=sid))
        

    
    
    return render_template('book.html',msg=msg,uname=uname,sid=sid,slot=slot)

@app.route('/tariff', methods=['GET', 'POST'])
def tariff():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    data= cursor.fetchone()
    return render_template('tariff.html',msg=msg, data=data, uname=uname)

@app.route('/history', methods=['GET', 'POST'])
def history():
    msg=""
    
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_booking b,ev_station s where b.station=s.id and b.uname=%s",(uname, ))
    data= cursor.fetchall()
    
    
    return render_template('history.html',msg=msg, data=data, uname=uname)

@app.route('/home', methods=['GET', 'POST'])
def home():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    data= cursor.fetchone()
    return render_template('home.html',msg=msg, data=data, uname=uname)

@app.route('/view', methods=['GET', 'POST'])
def view():
    msg=""
    if 'username' in session:
        uname = session['username']

    msg=""
    act=""
    rid=""
    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0
    s7=0
    s8=0
    s9=0
    s10=0
    if 'username' in session:
        uname = session['username']
    #if request.method=='GET':
    act=request.args.get('act')
    if act=="pay":
        rid=request.args.get('rid')
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set pay_st=2,status=3 where id=%s",(rid, ))
        mydb.commit()
        return redirect(url_for('view'))
    if act=="start":
        rid=request.args.get('rid')
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=2 where id=%s",(rid, ))
        mydb.commit()
        return redirect(url_for('view'))
        
        
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    dd= cursor.fetchone()
    station=dd[1]
    sid=dd[0]
    cursor.execute("SELECT * FROM ev_booking where station=%s and status=1",(sid, ))
    data= cursor.fetchall()

    for nn in data:
        if nn[5]==1:
            s1=1
        if nn[5]==2:
            s2=2
        if nn[5]==3:
            s3=3
        if nn[5]==4:
            s4=4
        if nn[5]==5:
            s5=5
        if nn[5]==6:
            s6=6
        if nn[5]==7:
            s7=7
        if nn[5]==8:
            s8=8
        if nn[5]==9:
            s9=9
        if nn[5]==10:
            s10=10
        
        
    
    act="ok"
    return render_template('view.html',msg=msg,uname=uname,sid=sid,station=station,act=act,data=data,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10)

@app.route('/charge1', methods=['GET', 'POST'])
def charge1():
    msg=""
    amt=0
    cost=0
    if 'username' in session:
        uname = session['username']

    rid=request.args.get('rid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    cmin=dd[17]
    csec=dd[18]
    plan=dd[8]
    
    if plan==1:
        cost=100
    elif plan==2:
        cost=200
    else:
        cost=300
        
    
    if csec<60:
        csec+=1
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
        

    else:
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=3,charge_time=30,charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
    if dd[19]==3:
        amt=cost
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=4,charge=%s where id=%s",(amt,rid))
        mydb.commit()
    
    return render_template('charge1.html',rid=rid, cmin=cmin, csec=csec)

@app.route('/charge2', methods=['GET', 'POST'])
def charge2():
    msg=""
    if 'username' in session:
        uname = session['username']
    amt=0
    cost=0
    rid=request.args.get('rid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    cmin=dd[17]
    
    csec=dd[18]
    print("sc="+str(csec))
    plan=dd[8]
    
    if plan==1:
        cost=100
    elif plan==2:
        cost=200
    else:
        cost=300
    
    if csec<60:
        csec+=1
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
        

    else:
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=3,charge_time=30,charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
    if dd[19]==3:
        amt=cost
        #+dd[15]
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=4,charge=%s where id=%s",(amt,rid))
        mydb.commit() 
    
    return render_template('charge2.html',rid=rid, cmin=cmin, csec=csec)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' in session:
        uname = session['username']
    amount=0
    rid=request.args.get('rid')
    sid=request.args.get('sid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    uu= cursor.fetchone()
    card=uu[6]
    mobile=uu[3]
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    amt=dd[15]
    ch=dd[15]

    t = time.localtime()
    rtime = time.strftime("%H:%M:%S", t)
    today= date.today()
    rdate= today.strftime("%d-%m-%Y")

    if ch>0:
        amount=ch
    else:
        amount=20

    cursor = mydb.cursor()
    cursor.execute("update ev_booking set edate=%s,etime=%s,amount=%s where id=%s",(rdate,rtime,amount,rid))
    mydb.commit()

    if request.method=='POST':
        pay_mode=request.form['pay_mode']
        if pay_mode=="Bank":
            rn=randint(1000, 9999)
            otp=str(rn)
            cursor = mydb.cursor()
            cursor.execute("update ev_booking set pay_mode=%s,sms_st=1,otp=%s where id=%s",(pay_mode,otp,rid))
            mydb.commit()
            
            return redirect(url_for('verify_otp',rid=rid))
        else:
            cursor = mydb.cursor()
            cursor.execute("update ev_booking set pay_mode=%s,pay_st=1 where id=%s",(pay_mode,rid))
            mydb.commit()
            return redirect(url_for('slot',sid=sid))
            
        
    return render_template('payment.html',sid=sid,rid=rid, uname=uname,amount=amount,card=card)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    msg=""
    if 'username' in session:
        uname = session['username']
    amount=0
    rid=request.args.get('rid')
    sid=request.args.get('sid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    uu= cursor.fetchone()
    mobile=uu[3]
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    key=dd[14]
    amount=dd[15]
    sms_st=dd[22]
    if sms_st==1:
        kk="Key: "+key
        #url="http://iotcloud.co.in/testsms/sms.php?sms=otp&name=User&otp="+key+"&mobile="+str(mobile)
        url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name=User&mess="+kk+"&mobile="+str(mobile)
        webbrowser.open_new(url)
        cursor.execute("update ev_booking set sms_st=0 where id=%s",(rid,))
        mydb.commit()
            
        #params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'RandDC', 'message':message, 'number':mobile})
        #url = "http://pay4sms.in/sendsms/?%s" % params
        #with urllib.request.urlopen(url) as f:
        #    print(f.read().decode('utf-8'))
        #    print("sent"+str(mobile))
                
    if request.method=='POST':
        otp=request.form['otp']
        if key==otp:
            
            cursor = mydb.cursor()
            cursor.execute("update ev_booking set pay_st=2,status=3 where id=%s",(rid,))
            mydb.commit()
            #cursor.execute("update ev_register set amount=amount-%s where uname=%s",(amount,uname))
            #mydb.commit()
            #return redirect(url_for('slot',sid=sid))
            msg="Amount Paid Successfully"
        
    return render_template('verify_otp.html',rid=rid,sid=sid,msg=msg)

@app.route('/report', methods=['GET', 'POST'])
def report():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    dd= cursor.fetchone()
    sid=dd[0]
    cursor.execute("SELECT * FROM ev_booking where station=%s",(sid, ))
    data= cursor.fetchall()
    return render_template('report.html',msg=msg, data=data, uname=uname)

@app.route('/eb', methods=['GET', 'POST'])
def eb():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    dd= cursor.fetchone()
    sid=dd[0]
    cursor.execute("SELECT * FROM ev_booking where charge_st>0 and slot<=5 and station=%s",(sid, ))
    data= cursor.fetchall()
    return render_template('eb.html',msg=msg, data=data, uname=uname)

@app.route('/solar', methods=['GET', 'POST'])
def solar():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    dd= cursor.fetchone()
    sid=dd[0]
    cursor.execute("SELECT * FROM ev_booking where charge_st>0 and slot>=5 and station=%s",(sid, ))
    data= cursor.fetchall()
    return render_template('solar.html',msg=msg, data=data, uname=uname)

@app.route('/map', methods=['GET', 'POST'])
def map():
    msg=""
    if 'username' in session:
        uname = session['username']
    if request.method=='GET':
        lat=request.args.get('lat')
        lon=request.args.get('lon')
    return render_template('map.html',msg=msg, lat=lat, lon=lon)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
