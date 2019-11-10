from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.htm')

@app.route('/result')
def resu():
   return render_template('result.htm')
@app.route('/process',methods = ['POST', 'GET'])
def condi():
    if request.method == 'POST':
        try:
            rolls = request.form['roll']
            sems = request.form['semm']
            with sql.connect("student.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                query = 'SELECT * FROM Subject INNER JOIN result on Subject.subjectcode = result.subjectcode WHERE result.rollno = ' + str(rolls) + ' AND result.semester = ' + str(sems)
                cur.execute(query) 
                data = cur.fetchall()
                cur1 = con.cursor()
                q1 = "select * from SName where rollno=" + str(rolls) 
                cur1.execute(q1)
                data1= cur1.fetchall()
                cur2 = con.cursor()
                q2= "select * from Total where rollno=" + str(rolls) + " and sem=" + str(sems)
                cur2.execute(q2)
                data2= cur2.fetchall()
                return render_template("display.htm",data1=data1,data = data,data2 = data2) 

        except:
            con.rollback()
            return render_template('result.htm') 
            con.close() 
@app.route('/login')
def reu():
   return render_template('log_in.htm')
@app.route("/bmw",methods = ['POST', 'GET'])            
def login():
    error = None
    if request.method == 'POST':
        username = request.form['used']
        password = request.form['passed']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
            return render_template('log_in.htm',error=error)
        else:
            return render_template('data_entry.htm')
def validate(username, password):
    completion = False
    with sql.connect("student.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        q1 = "select usern from Techc where pword =" + "'" + str(password) + "'"
        cur.execute(q1)
        rows = cur.fetchall()
        if len(rows)==0:
            return completion 
        else:
            completion = True    
    return completion
    con.close()
@app.route('/dentry')
def dent():
   return render_template('data_entry.htm')    
@app.route("/dataentry",methods = ['POST', 'GET'])
def dentry():
    if request.method == 'POST':
      try:
         sem = request.form['semester']
         codes = request.form['code']
         rolls = request.form['roll']
         subs = request.form['subgp']
         grades = request.form['grade']
         with sql.connect("student.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO result (semester,subjectcode,rollno,subgp,grade) VALUES (?,?,?,?,?)",(sem,codes,rolls,subs,grades) )
            con.commit()
            msg= "Submitted Successfully !"
            dex = "select max(Sno) from result"
            cur.execute(dex)
            msgx=cur.fetchall()
            return render_template('data_entry.htm',msg=msg,msgx=msgx,msg1=sem,msg2=codes,msg3=rolls,msg4=subs,msg5=grades)
      except:
         con.rollback()
         msg= "Submitted UNSuccessfully !"
         return render_template('data_entry.htm',msg=msg)
         con.close()  
@app.route('/deletedata')
def delete():
   return render_template('delete_data.htm')   
@app.route("/delete",methods = ['POST', 'GET'])  
def dell():
    if request.method == 'POST':
        try:
            ind = request.form['index']
            with sql.connect("student.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                query ='DELETE FROM result WHERE sno = ' + str(ind)
                cur.execute(query) 
                con.commit()
                msg = "Deleted Successfully !"
                return render_template("delete_data.htm",msg=msg) 
        except:
            con.rollback()
            msg="Not Deleted ,Try Again !"
            return render_template('delete_data.htm',msg=msg) 
            con.close() 
@app.route('/signupp')
def d():
   return render_template('sign_up.htm')   
@app.route("/signup",methods = ['POST', 'GET'])
def sup():
    if request.method == 'POST':
      try:
         nn = request.form['uname']
         pp = request.form['pasw']
         mm = request.form['mno']
        
         with sql.connect("student.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Techc (usern,pword,mobile) VALUES (?,?,?)",(nn,pp,mm) )
            con.commit()
            msg= "Sign up Successfully !"
            return render_template('sign_up.htm',msg=msg)
      except:
         con.rollback()
         msg= "Sign up unsuccessfull !"
         return render_template('sign_up.htm',msg=msg)
         con.close()  
@app.route('/alert')
def fcmp():
   return render_template('alert.htm')   
@app.route("/alarm",methods = ['POST', 'GET'])
def fcm():
    if request.method == 'POST':
      try:
         msgs = request.form['msg']
         with sql.connect("student.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select mesg from SName" )
            
            data = cur.fetchall()
            API_KEY = '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'
           
            message = Mail(from_email='amit1004199@gmail.com',to_emails=str(data),subject='checking',html_content= str(msgs))
         
            sg = SendGridAPIClient(API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
             
            msg= "Message sent Successfully !"
            return render_template('alert.htm',msg=msg)
      except:
         con.rollback()
         msg= "Message sent unsuccessfull !"
         return render_template('alert.htm',msg=msg)
         con.close()  

if __name__ == '__main__':
    app.run(debug = True)         