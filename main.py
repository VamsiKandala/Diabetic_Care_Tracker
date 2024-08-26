from flask import Flask, request, redirect,render_template,session,url_for,flash
import mysql.connector
import random
import math,re,os
from key import secret_key,salt
from itsdangerous import URLSafeTimedSerializer
from stoken import token
from cmail import sendmail
import flask_excel as excel
import pyxlsb
import pyexcel
import io
import sys

import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)
app.secret_key =secret_key
excel.init_excel(app)




mydb=mysql.connector.connect(host="localhost",user="root",password="vamsi",db="diabapp")
cursor=mydb.cursor()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def checkvalidemail(usermail):
    if(re.fullmatch(regex, usermail)):
        return True
 
    else:
        return False
def checkvalidpassword(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    val = True
    message=''
              
    if not any(char.isdigit() for char in passwd):
        flash('Password should have at least one numeral.')
        val = False
        return render_template('uregistration.html')
         
    if not any(char.isupper() for char in passwd):
        flash('Password should have at least one uppercase letter')
        val = False
        return render_template('uregistration.html')
         
    if not any(char.islower() for char in passwd):
        flash('Password should have at least one lowercase letter.')
        val = False
        return render_template('uregistration.html')
         
    if not any(char in SpecialSym for char in passwd):
        flash('Password should have at least one of the symbols $@#')
        val = False
        return render_template('uregistration.html')
    if val: 
        return val

def checkresetpassword(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    val = True
    message=''
              
    if not any(char.isdigit() for char in passwd):
        flash('Password should have at least one numeral.')
        val = False
        return render_template('resetpassword.html')
         
    if not any(char.isupper() for char in passwd):
        flash('Password should have at least one uppercase letter')
        val = False
        return render_template('resetpassword.html')
         
    if not any(char.islower() for char in passwd):
        flash('Password should have at least one lowercase letter.')
        val = False
        return render_template('resetpassword.html')
         
    if not any(char in SpecialSym for char in passwd):
        flash('Password should have at least one of the symbols $@#')
        val = False
        return render_template('resetpassword.html')
    if val: 
        return val

def checkresetpassword1(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    val = True
    message=''
              
    if not any(char.isdigit() for char in passwd):
        flash('Password should have at least one numeral.')
        val = False
        return render_template('resetpassword1.html')
         
    if not any(char.isupper() for char in passwd):
        flash('Password should have at least one uppercase letter')
        val = False
        return render_template('resetpassword1.html')
         
    if not any(char.islower() for char in passwd):
        flash('Password should have at least one lowercase letter.')
        val = False
        return render_template('resetpassword1.html')
         
    if not any(char in SpecialSym for char in passwd):
        flash('Password should have at least one of the symbols $@#')
        val = False
        return render_template('resetpassword1.html')
    if val: 
        return val

def checkresetpassword2(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    val = True
    message=''
              
    if not any(char.isdigit() for char in passwd):
        flash('Password should have at least one numeral.')
        val = False
        return render_template('resetpassword2.html')
         
    if not any(char.isupper() for char in passwd):
        flash('Password should have at least one uppercase letter')
        val = False
        return render_template('resetpassword2.html')
         
    if not any(char.islower() for char in passwd):
        flash('Password should have at least one lowercase letter.')
        val = False
        return render_template('resetpassword2.html')
         
    if not any(char in SpecialSym for char in passwd):
        flash('Password should have at least one of the symbols $@#')
        val = False
        return render_template('resetpassword2.html')
    if val: 
        return val



@app.route('/')
def h1():
    return redirect(url_for('home'))
@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
        usermail=request.form['email']
        up=request.form['password1']
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from userdata where email=%s and password=%s",(usermail,up))
        record=cursor.fetchone()[0]
        print(record)
        if record==1:
            session['loggedin']=True
            session['usermail']=usermail
            cursor.close()
            return redirect(url_for('userview'))
        
        else:
            flash('Invalid Username/Password')
            return render_template('userlogin.html')
        
    return render_template('userlogin.html')

@app.route('/userregistration',methods=['GET','POST'])
def userregistration():
    if request.method == 'POST':
        cursor=mydb.cursor(buffered=True)
        uname=request.form['name']
        usermail=request.form['email']
        udob=request.form['date']
        upass1=request.form['password1']
        upass2=request.form['password2']
        umobile=request.form['mobile']
        ugender=request.form['gender']
        usqa1=request.form['sqa1']
        usqa2=request.form['sqa2']
        usqa3=request.form['sqa3']
        usqa4=request.form['sqa4']
        usqa5=request.form['sqa5']
        usqa6=request.form['sqa6']
        cursor.execute('select count(*) from userdata where name=%s',[uname])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from userdata where email=%s',[usermail])
        count1=cursor.fetchone()[0]
        cursor.close()
        if upass1!=upass2:
            flash('Password not matched.')
            return render_template('uregistration.html')

        if count==1:
            flash('username already in use')
            return render_template('uregistration.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('uregistration.html')
        checkvalidemail(usermail)
        checkvalidpassword(upass2)
        if checkvalidemail(usermail)==False:
            flash('Invalid Email Format')
            return render_template('uregistration.html')
        if checkvalidpassword(upass2)==False:
            flash('The must password must be length of 8-15 and having atleast One UpperCase,One LowerCase,One Special Character $@#')
            return render_template('uregistration.html')

        if (checkvalidemail(usermail) and checkvalidpassword(upass2))==True:
            data={'username':uname,'password':upass2,'email':usermail,'dob':udob,'gender':ugender,'mobile':umobile,'sqa1':usqa1,'sqa2':usqa2,'sqa3':usqa3,'sqa4':usqa4,'sqa5':usqa5,'sqa6':usqa6}
            subject='Email Confirmation'
            body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(data),_external=True)}"
            sendmail(to=usermail,subject=subject,body=body)
            flash('Confirmation link sent to mail')
            return redirect(url_for('userlogin'))

        
        
    return render_template('uregistration.html')

@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        #print(e)
        return 'Link Expired register again'
    else:
        cursor=mydb.cursor(buffered=True)
        username=data['username']
        cursor.execute('select count(*) from userdata where name=%s',[username])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('login'))
        else:
            cursor.execute('insert into userdata values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[data['username'],data['email'],data['dob'],data['gender'],data['mobile'],data['sqa1'],data['sqa2'],data['sqa3'],data['sqa4'],data['sqa5'],data['sqa6'],data['password']])
            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('userlogin'))  
         
@app.route('/userview',methods=['GET','POST'])
def userview():
    usermail=[session.get('usermail')]
    cursor=mydb.cursor(buffered=True)
    cursor.execute("select time,phrase,meal,menu,grams,readings from userfood where usermail=%s",(usermail))
    record=cursor.fetchall()
    if record:
        cursor.close()
        return render_template('user_view.html',value=record)
    return render_template('user_view.html')

cursor=mydb.cursor(buffered=True)
@app.route('/userreadings',methods=['GET','POST'])
def userreadings():
    if request.method == 'POST':
        utime=request.form['ut']
        uphrase=request.form['a1']
        unmail=session.get('usermail')
        umeal=request.form['m1']
        umenu=request.form['b1']
        ugrams=request.form['b2']
        ureadings=request.form['c1']
        
        data={'time':utime,'phrase':uphrase,'meal':umeal,'usermail':unmail,'menu':umenu,'grams':ugrams,'readings':ureadings,'a':""}
        cursor=mydb.cursor(buffered=True)
        
        cursor.execute("select email,name from userdata where email=%s",([data['usermail']]))
        emailrec=cursor.fetchone()
        if emailrec:
            if uphrase=='FBS':
                result=cursor.execute("insert into userfood values(%s,%s,%s,%s,%s,%s,%s)",[data['time'],data['phrase'],data['meal'],data['usermail'],data['menu'],data['grams'],data['readings']])
                mydb.commit()
                cursor.close()
                return redirect(url_for('userview'))
            
            if uphrase=='PP':
                result=cursor.execute("insert into userfood values(%s,%s,%s,%s,%s,%s,%s)",[data['time'],data['phrase'],data['meal'],data['usermail'],data['menu'],data['grams'],data['readings']])
                mydb.commit()
                se=cursor.execute('select readings from userfood where usermail=%s',([data['usermail']]))
                mydb.commit()
                cursor.close()
                return redirect(url_for('userview'))
            

            
        else:
            cursor.close()
            return render_template('NewBloodReadings.html')
        
    return render_template('NewBloodReadings.html')

@app.route('/resetpassword',methods=['GET','POST'])
def resetpassword():
    if request.method == 'POST':
        usermail=request.form['email']
        uop=request.form['password1']
        unp=request.form['password2']
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from userdata where email=%s and password=%s",(usermail,uop))
        record=cursor.fetchone()[0]
        print(record)
        if record==1:
            checkresetpassword(unp)
            if checkresetpassword(unp)==True:
                cursor.execute('select password from userdata where email=%s',[(usermail)])
                ab=cursor.fetchone()[0]
                if unp==ab:
                    flash('Entered Password is Matched With the Old Password.Try Another One')
                    return render_template('resetpassword1.html')
                else:
                    q=cursor.execute('update userdata set password=%s where email=%s',(unp,usermail))
                    mydb.commit()
                    flash('Password Updated.')
                    return redirect(url_for('userlogin'))
        
        else:
            flash('Invalid Username/Password')
            return render_template('resetpassword.html')
        
    return render_template('resetpassword.html')

@app.route('/resetpassword1',methods=['GET','POST'])
def resetpassword1():
    if request.method == 'POST':
        usermail=request.form['email']
        usqa1=request.form['sqa1']
        usqa2=request.form['sqa2']
        usqa3=request.form['sqa3']
        usqa4=request.form['sqa4']
        usqa5=request.form['sqa5']
        usqa6=request.form['sqa6']
        unp=request.form['newp']
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from userdata where email=%s",[(usermail)])
        record=cursor.fetchone()[0]
        if record==1:
            cursor.execute('select sq1,sq2,sq3,sq4,sq5,sq6 from userdata where email=%s',[usermail])
            s=[list(i) for i in cursor.fetchall()]
            for c in s:
                if(c[0]==usqa1 and c[1]==usqa2 and c[2]==usqa3 and c[3]==usqa4 and c[4]==usqa5 and c[5]==usqa6):
                    checkresetpassword1(unp)
                    if checkresetpassword1(unp)==True:
                        cursor.execute('select password from userdata where email=%s',[(usermail)])
                        ab=cursor.fetchone()[0]
                        if unp==ab:
                            flash('Entered Password is Matched With the Old Password.Try Another One')
                            return render_template('resetpassword1.html')
                        else:
                            q=cursor.execute('update userdata set password=%s where email=%s',(unp,usermail))
                            mydb.commit()
                            flash('Password Updated.')
                            return redirect(url_for('userlogin'))
        
        else:
            flash('Invalid Username/Password/Security Question/Security Question Answer ')
            return render_template('resetpassword1.html')
        
    return render_template('resetpassword1.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        flash('Successfully logged out')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    
@app.route('/balanceddiet')
def balanceddiet():
    return render_template('balanceddiet.html')

@app.route('/downloadreport',methods=["GET","POST"])
def downloadreport():
    cursor=mydb.cursor(buffered=True)
    a=session.get('usermail')
    cursor.execute("select time,phrase,meal,menu,grams,readings from userfood where usermail=%s",[(a)])
    data1=cursor.description
    lst=[i[0] for i in data1]
    cursor.execute("select time,phrase,meal,menu,grams,readings from userfood where usermail=%s",[(a)])
    data=[list(i) for i in cursor.fetchall()]
    #print(data)
    data.insert(0,lst)
    #return (data)
    return excel.make_response_from_array(data, "csv",file_name="Glucose_report")

@app.route('/analysisreport',methods=["GET","POST"])
def analysisreport():
    cursor=mydb.cursor(buffered=True)
    user=session.get('usermail')
    cursor.execute("select menu,readings from userfood where usermail=%s",[user])
    data = cursor.fetchall()

    x_values = [row[0] for row in data]
    y_values = [row[1] for row in data]
    

    plt.bar(x_values, y_values)
    plt.xlabel('Menu')
    plt.ylabel('Glucose Levels')
    plt.title('Data Visualization Of Food taken')
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the plot to a temporary file
    plot_path = 'static/temp_plot.png'
    plt.savefig(plot_path)
    plt.close()

    return render_template('analysisreport.html', plot_path=plot_path)

@app.route('/resetpassword2',methods=["GET","POST"])
def resetpassword2():
    if request.method=="POST":
        usermail=request.form['email']
        unp=request.form['newp']
        ufood=request.form['food']
        uthing=request.form['things']
        uvehicle=request.form['vehicles']
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from userdata where email=%s",[(usermail)])
        record=cursor.fetchone()[0]
        if record==1:
            cursor.execute("select * from pic")
            s=[list(i) for i in cursor.fetchall()]
            for c in s:
                if(c[0]==ufood and c[1]==uthing and c[2]==uvehicle):
                    checkresetpassword2(unp)
                    if checkresetpassword2(unp)==True:
                        cursor.execute('select password from userdata where email=%s',[(usermail)])
                        ab=cursor.fetchone()[0]
                        if unp==ab:
                            flash('Entered Password is Matched With the Old Password.Try Another One')
                            return render_template('resetpassword2.html')
                        else:
                            q=cursor.execute('update userdata set password=%s where email=%s',(unp,usermail))
                            mydb.commit()
                            flash('Password Updated.')
                            return redirect(url_for('userlogin'))
                else:
                    flash('Invalid Username/Selected Pictures Not Matched ')
                    return render_template('resetpassword2.html')

        
        
        
    return render_template("resetpassword2.html")

@app.route('/displaynames',methods=["GET","POST"])
def displaynames():
    food=['bread','idli','meat']
    thing=['laptop','mobile','watch']
    vehicles=['bike','car','bus']
    a=random.choice(food)
    b=random.choice(thing)
    c=random.choice(vehicles)
    cursor=mydb.cursor(buffered=True)
    d=cursor.execute("update pic set food=%s,thing=%s,vehicles=%s",(a,b,c))
    mydb.commit()
    flash(f"Select the Following pictures of {a},{b},{c}")
    return redirect(url_for('resetpassword2'))


    




if __name__ == '__main__':
    app.run(debug=True)
