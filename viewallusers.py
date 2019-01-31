import os
from flask import Flask, render_template, request
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app=Flask(__name__)
engine=create_engine(os.environ['DATABASE_URL'])
db=scoped_session(sessionmaker(bind=engine))

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



@app.route('/')
def index():
	return render_template("homepage.html")


@app.route('/viewallusers')
def viewusers():
	data=db.execute("SELECT * FROM users").fetchall()
	db.commit()
	return render_template("viewallusers.html", data=data)

@app.route('/user')
def user():
	return render_template("userfound.html",idfrom=request.args.get('userid')
		,name=request.args.get('name'),email=request.args.get('email'),current_credit=request.args.get('current_credit'))

@app.route('/transfer')
def transfer():
	data=db.execute("SELECT * FROM users").fetchall()
	db.commit()
	print(request.args.get('userid'))
	return render_template("transfer.html", data=data,idfrom=request.args.get('idfrom'),current_creditfrom=request.args.get('current_creditfrom'))


@app.route('/credit_transfer')
def credit_transfer():
	return render_template("credit_transfer.html",idto=request.args.get('idto'),
		name=request.args.get('name'),current_creditto=request.args.get('current_creditto'),idfrom=request.args.get('idfrom'),current_creditfrom=request.args.get('current_creditfrom'))


@app.route('/do_transfer')
def do_transfer():
	idto=request.args.get('idto')
	print(idto)
	idfrom=request.args.get('idfrom')
	transfer_amount=request.args.get('amount')
	data=db.execute("SELECT * FROM users").fetchall()
	db.commit()
	db.execute("UPDATE users SET current_credit=current_credit-:amount WHERE id=:idfrom",{"idfrom":idfrom,"amount":transfer_amount})
	db.execute("UPDATE users SET current_credit=current_credit+:amount WHERE id= :idto",{"idto":idto,"amount":transfer_amount})
	db.execute("INSERT INTO transfers (transaction_from, transaction_to, amount) VALUES (:transaction_from, :transaction_to, :amount)",
	  {"transaction_from":int(idfrom), "transaction_to":int(idto) ,"amount" :transfer_amount})
	db.commit()
	data=db.execute("SELECT * FROM users").fetchall()
	db.commit()
	return render_template("viewallusers.html",data=data)

if __name__ == '__main__':
	app.run()
