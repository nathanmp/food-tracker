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

colors = [{'name':'Water', 'color':'blue', 'serving':'1 cup', 'cal':0, 'fat':0, 'protein': 0, 'carbs': 0, 'id': 0},
{'name':'Tea/Coffee', 'color':'blue', 'serving':'1 cup', 'cal':0, 'fat':0, 'protein': 0, 'carbs': 0, 'id': 2},
{'name':'Green vegetables', 'color':'green', 'serving':'1 cup', 'cal':25, 'fat':0, 'protein': 5, 'carbs': 2, 'id': 3},
{'name':'Starchy vegetables', 'color':'green', 'serving':'1/2 cup', 'cal':80, 'fat':0, 'protein': 15, 'carbs': 3, 'id': 4},
{'name':'Potatoes', 'color':'red', 'serving':'4 oz', 'cal':100, 'fat':0, 'protein': 21, 'carbs': 3, 'id': 5},
{'name':'Fruit', 'color':'green', 'serving':'1/2 cup', 'cal':60, 'fat':0, 'protein': 15, 'carbs': 0, 'id': 6},
{'name':'Beans', 'color':'green', 'serving':'1/2 cup', 'cal':125, 'fat':2, 'protein': 15, 'carbs': 7, 'id': 7},
{'name':'Poultry', 'color':'green', 'serving':'3 oz', 'cal':45, 'fat':3, 'protein': 0, 'carbs': 28, 'id': 8},
{'name':'Seafood', 'color':'green', 'serving':'3 oz', 'cal':100, 'fat':10, 'protein': 0, 'carbs': 19, 'id': 9},
{'name':'Fruit juice', 'color':'yellow', 'serving':'1/2 cup', 'cal':60, 'fat':0, 'protein': 15, 'carbs': 0, 'id': 10},
{'name':'Nuts', 'color':'yellow', 'serving':'1 oz', 'cal':160, 'fat':12, 'protein': 9, 'carbs': 5, 'id': 11},
{'name':'Eggs', 'color':'yellow', 'serving':'1', 'cal':75, 'fat':4, 'protein': 0, 'carbs': 7, 'id': 12},
{'name':'Cheese', 'color':'yellow', 'serving':'1 oz', 'cal':100, 'fat':5, 'protein': 0, 'carbs': 7, 'id': 13},
{'name':'Milk', 'color':'green', 'serving':'1 cup', 'cal':120, 'fat':5, 'protein': 15, 'carbs': 8, 'id': 14},
{'name':'Yogurt', 'color':'green', 'serving':'1 pkg', 'cal':120, 'fat':5, 'protein': 15, 'carbs': 8, 'id': 15},
{'name':'Sauces', 'color':'yellow', 'serving':'1 tbsp', 'cal':45, 'fat':5, 'protein': 0, 'carbs': 0, 'id': 16},
{'name':'Red meat', 'color':'red', 'serving':'1 oz', 'cal':100, 'fat':8, 'protein': 0, 'carbs': 7, 'id': 18},
{'name':'Deli meat', 'color':'red', 'serving':'1 oz', 'cal':45, 'fat':9, 'protein': 0, 'carbs': 7, 'id': 19},
{'name':'Oils', 'color':'red', 'serving':'1 tsp', 'cal':45, 'fat':5, 'protein': 0, 'carbs': 0, 'id': 20},
{'name':'Bread', 'color':'yellow', 'serving':'1 slice', 'cal':80, 'fat':0, 'protein': 15, 'carbs': 3, 'id': 21},
{'name':'Processed Grains', 'color':'red', 'serving':'1/2 cup', 'cal':80, 'fat':0, 'protein': 15, 'carbs': 3, 'id': 22},
{'name':'Dairy desserts', 'color':'red', 'serving':'1/2 cup', 'cal':130, 'fat':7, 'protein': 15, 'carbs': 3, 'id': 23},
{'name':'Other desserts', 'color':'red', 'serving':'2 oz', 'cal':220, 'fat':11, 'protein': 30, 'carbs': 2, 'id': 24},
{'name':'Soda', 'color':'red', 'serving':'8 oz', 'cal':100, 'fat':0, 'protein': 26, 'carbs': 0, 'id': 25}]

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
