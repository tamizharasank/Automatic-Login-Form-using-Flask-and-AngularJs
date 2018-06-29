import os
import datetime
import MySQLdb
import hashlib
m = hashlib.md5()
con=MySQLdb.connect("localhost","root","root","pana")
cursor=con.cursor()
from flask import Flask,request,render_template,session,redirect,jsonify,send_from_directory
app=Flask(__name__)
app.secret_key = "tam"
#LOGIN SESSION
@app.route("/")
def login():
	return render_template("login.html")
@app.route("/register")
def register():
	return render_template("register.html")	
@app.route("/login_validate",methods=['POST'])
def login_validate():
	data= request.get_json()
	user_id=data.get("user_name")
	password=data.get("password")
	password=hashlib.md5(password.encode("utf")).hexdigest()	
	print user_id,password
	cursor.execute("SELECT * FROM register WHERE mobile='%s' AND password='%s'" %(user_id,password))
	data=cursor.fetchone()
	print data
	if data==None:
		re="n"	
	else:
		session['user_id']=user_id
		# user=session['user_id']
		re="s"
	return re
@app.route("/register.json",methods=['POST'])
def add():
	data=request.get_json()
	name=data.get("name")
	address=data.get("address")
	password=data.get("password")
	m.update(password.encode('utf-8'))
	password=m.hexdigest()
	dob=data.get("dob")
	roll=data.get("roll")
	city=data.get("city")
	mobile=data.get("mobile")
	email=data.get("email")
	state=data.get("state")
	cursor.execute("INSERT INTO register (`name`,`email`,`password`,`roll`,  `state`,`city`,`address`,`dob`,`mobile`) values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " %(name,email, password,roll,state, city,address,dob,mobile))
	con.commit()	
	return "Insert Record Successfully"
@app.route("/city.json")
def city():
		cursor.execute("SELECT * FROM city")		
		des=[]
		i=[]
		for y in cursor.description:
	 		des.append(y[0])
	 	for x in cursor.fetchall():
	 		i.append({des[1]:x[1],des[2]:x[2]})	
		# print i
		return jsonify(i)
@app.route("/state.json")
def state():
		cursor.execute("SELECT * FROM state")
		des=[]
		i=[]
		for y in cursor.description:
	 		des.append(y[0])
	 	for x in cursor.fetchall():
	 		i.append({des[0]:x[0],des[1]:x[1]})	
		# print i
		return jsonify(i)	  	
@app.route("/getdata")
def getdata():
		user_id=session['user_id']
		cursor.execute("SELECT register.name, register.email, register.roll, register.address,register.dob,register.mobile, s.state,c.city FROM register JOIN state as s on register.state = s.no JOIN city as c ON register.city = c.id WHERE register.mobile = '%s'"%(user_id))
		x=cursor.fetchone()
		des=[]
		for y in cursor.description:
	 		des.append(y[0])	  
		data={des[0]:x[0],des[1]:x[1],des[3]:x[3],des[4]:x[4],des[5]:x[5],des[6]:x[6],des[7]:x[7]}	
		print data
		return jsonify(data)
@app.route("/view")
def view():
	user_id=session['user_id']
	return render_template("user.html",user=user_id)
@app.route("/logout")
def logout():
	session.pop('user_id',None)
	return redirect("/")
	
if __name__=="__main__":

	app.run("tamizh",88,debug=True)
	



	
