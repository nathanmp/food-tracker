from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user
from flask_login.mixins import AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3
import json
import sys
import os
from eatr import db
from eatr import app, models
from eatr.models import User
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
	print(user_id, file=sys.stderr)
	print(u, file=sys.stderr)
	return u

colors = [{"name": "Green veggies", "color": "green", "serv": "1 cup", "id":"1"},
		{"name": "Root veggies", "color": "green", "serv": "1 cup", "id":"2"},
		{"name": "Berries", "color": "green", "serv": "1/2 cup", "id":"3"},
		{"name": "Sphere fruit", "color": "green", "serv": "1", "id":"4"},
		{"name": "Beans", "color": "yellow", "serv": "1/2 cup", "id":"5"},
		{"name": "Nuts", "color": "yellow", "serv": "1/2 oz", "id":"6"},
		{"name": "Poultry", "color": "yellow", "serv": "3 oz", "id":"7"},
		{"name": "Seafood", "color": "yellow", "serv": "3 oz", "id":"8"},
		{"name": "Red meat", "color": "red", "serv": "3 oz", "id":"9"},
		{"name": "Deli meat", "color": "red", "serv": "2 oz", "id":"10"},
		{"name": "Eggs", "color": "yellow", "serv": "1", "id":"11"},
		{"name": "Cheese", "color": "yellow", "serv": "1/4 cup", "id":"12"},
		{"name": "Yogurt", "color": "yellow", "serv": "1 cup", "id":"13"},
		{"name": "Milk", "color": "yellow", "serv": "1 cup", "id":"14"},
		{"name": "Wheat", "color": "yellow", "serv": "1 cup", "id":"15"},
		{"name": "Oils", "color": "red", "serv": "2 tbsp", "id":"16"},
		{"name": "Heavy sauces", "color": "red", "serv": "2 tbsp", "id":"17"},
		{"name": "Light sauces", "color": "yellow", "serv": "2 tbsp", "id":"18"},
		{"name": "Bread", "color": "yellow", "serv": "1 slice", "id":"19"},
		{"name": "Grains", "color": "yellow", "serv": "1 cup", "id":"20"},
		{"name": "Desserts", "color": "red", "serv": "1 oz", "id":"21"}]

@app.route("/")
@app.route("/home")
def addpg():
	if current_user.is_anonymous:
		return redirect("/signuporin")
	else:
		return render_template("food.html", title="Home", foods=colors, cuser=current_user)

@app.route("/stats")
def stats():
	if current_user.is_authenticated:
		feq = models.FoodElement.query.filter_by(uid=current_user.username).all()
	else:
		feq = models.FoodElement.query.filter_by(uid="Guest").all()
	return render_template("stats.html", title="Stats", foodelems=feq)

@app.route("/addfood", methods=["POST"])
def addfood():
	data = request.get_json()
	f = models.FoodElement(data['id'], data['serving'], data['username'])
	print(f)
	db.session.add(f)
	db.session.commit()
	return ""
	
@app.route("/signinuser", methods=["POST"])
def signinuser():
	if current_user.is_authenticated:
		return redirect(url_for("/home"))
	print(str(request.form), file=sys.stderr)
	u = User.query.filter_by(username=request.form['username']).first()
	if u is None or not u.check_password(request.form['password']):
		flash("Incorrect details.")
		return redirect(url_for("/signuporin"))
	elif u.check_password(request.form['password']):
		login_user(u, remember=True)
		return redirect("/home")
	else:
		return redirect("/signuporin")

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

@app.route("/signup", methods=["GET", "POST"])
def signuppg():
	if request.method == "GET":
		return render_template("signup.html")
	res = signupuser()
	if res:
		return redirect("/home")
	else:
		return redirect("/signup")
		
@app.route("/logout")
def logout():
	logout_user()
	return redirect("/home")

@app.route("/signuporin", methods=["GET"])
def sorl():
	return render_template("signuporin.html")
