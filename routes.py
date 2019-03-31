from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login.mixins import AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3
import json
import sys
import os
import datetime
from eatr import db, app, models
app = Flask('eatr')
app.debug = True
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	u = models.User.query.filter_by(username=user_id).first()
	return u

@app.route("/")
@app.route("/home")
def addpg():
	if current_user.is_anonymous:
		return redirect("/signuporin")
	else:
		flist = current_user.foodtypes
		colors = []
		for i in flist:
			colors.append({"name":i.food_name, "id":i.ftid, "color":i.color, "serving":i.serv_name,
				"protein":i.protein_amt, "fat":i.fat_amt, "carbs":i.carb_amt, "calories":i.calories})
		print(str(colors), file=sys.stderr)
		return render_template("index.html", title="Home", foods=colors, cuser=current_user)

@app.route("/stats/", defaults={"timeframe":-1})
@app.route("/stats/<int:timeframe>")
def stats(timeframe):
	if timeframe == -1:
		timediff = datetime.datetime.utcnow() - datetime.datetime(2019, 3, 1)
	else:
		timediff = datetime.datetime.utcnow() - datetime.timedelta(days=timeframe)
	if current_user.is_authenticated:
		feq = models.FoodElement.query.filter(models.FoodElement.timestamp > timediff,\
		models.FoodElement.uid==current_user.username).all()
	else:
		feq = models.FoodElement.query.filter_by(uid="Guest").all()
	return render_template("stats.html", title="Stats", foodelems=feq)

@app.route("/signup", methods=["GET"])
def signuppg():
	return render_template("signup.html")


@app.route("/signuporin", methods=["GET"])
def sorl():
	return render_template("signuporin.html")

def deletefood(food_id):
	fe = models.FoodElement.query.filter_by(eid=food_id).first()
	if fe.uid == current_user.username:
		db.session.delete(fe)
		db.session.commit()
	return redirect('/stats')
	
@app.route("/logout")
def logout():
	logout_user()
	return redirect("/home")

@app.route("/signupuser", methods=["POST"])
def signupuser():
	data = request.form
	print(data['username'])
	u = models.User(data['username'], data['email'])
	u.set_password(data['password'])
	db.session.add(u)
	db.session.commit()
	login_user(u, remember=True)
	flash("Signed up.")
	return redirect("/home")

@app.route("/signinuser", methods=["POST"])
def signinuser():
	if current_user.is_authenticated:
		return redirect(url_for("/home"))
	u = models.User.query.filter_by(username=request.form['username']).first()
	if u is None or not u.check_password(request.form['password']):
		flash("Incorrect details.")
		return redirect(url_for("/signuporin"))
	elif u.check_password(request.form['password']):
		login_user(u, remember=True)
		return redirect("/home")
	else:
		return redirect("/signuporin")

@app.route("/addfood", methods=["POST"])
def addfood():
	data = request.get_json()
	m = models.Meal(timestamp=datetime.utcnow())
	db.session.add(m)
	db.session.commit()
	l = []
	for i in data:
		m = models.FoodElement(i['id'], i['serving'], i['username'], mealid=m)
		l.append(m)
	db.session.commit()
	return ""
