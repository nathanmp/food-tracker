from flask import Flask, request, render_template
from flask_login import LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3
import json
import sys
import os
from eatr import db
from eatr import app, models
app.secret_key = "REDACTED"
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
	return models.User.query.filter_by(email=user_id).first()
colors = [{"name": "Green and cruciferous vegetables", "color": "green", "serv": "1 cup", "id":"1"},
		{"name": "Root vegetables and gourds", "color": "green", "serv": "1 cup", "id":"2"},
		{"name": "Berries and stone fruit", "color": "green", "serv": "1/2 cup", "id":"3"},
		{"name": "Apples, oranges, and pears", "color": "green", "serv": "1", "id":"4"},
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
def addpg():
	if not current_user.is_authenticated:
		return render_template("signup.html")
	else:
		return render_template("food.html", title="Home", foods=colors, cuser=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":	
		if current_user.is_authenticated:
			return redirect(url_for("/"))
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.username.data).first()
			if user is None or not user.check_password(form.password.data):
				return redirect(url_for("/"))
		return 0
	else:
		##login code here
		return 0

@app.route("/signup")
def signup():
	return 0

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
	print(request.get_json(), file=sys.stderr)
	f = models.FoodElement(data['id'], data['serving'], data['username'])
	print(f)
	db.session.add(f)
	db.session.commit()
	return render_template("food.html", title="Home", foods=colors)

@app.route("/adduser", methods=["POST"])
def adduser():
	data = request.get_json()
	print(request.get_json(), file=sys.stderr)
	u = models.User(data['uname'], data['email'])
	u.set_password(data['passwd'])
	db.session.add(u)
	db.session.commit()
	login_user(u)
	return render_template('food.html')
@app.route("/login", methods=["POST"])
def loginuser():
	return 0
