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
		if flist == []:
			s = """Water|blue|1 cup|0|0|0|0
			Tea|blue|1 cup|0|0|0|0
			Coffee|blue|1 cup|0|0|0|0
			Green vegetables|green|1 cup|25|0|5|2
			Starchy vegetables|green|1/2 cup|80|0|15|3
			Potatoes|red|4 oz|100|0|21|3
			Fruit|green|1/2 cup|60|0|15|0
			Beans|green|1/2 cup|125|2|15|7
			Poultry|green|3 oz|45|3|0|28
			Seafood|green|3 oz|100|10|0|19
			Fruit juice|yellow|1/2 cup|60|0|15|0
			Nuts|yellow|1 oz|160|12|9|5
			Eggs|yellow|1|75|4|0|7
			Cheese|yellow|1 oz|100|5|0|7
			Milk|green|1 cup|120|5|15|8
			Yogurt|green|1 pkg|120|5|15|8
			Light sauces|yellow|1 tbsp|45|5|0|0
			Heavy sauces|red|1 tbsp|45|5|0|0
			Red meat|red|1 oz|100|8|0|7
			Deli meat|red|1 oz|45|9|0|7
			Oils|red|1 tsp|45|5|0|0
			Bread|red|1 slice|80|0|15|3
			Processed Grains|red|1/2 cup|0|15|3|0
			Dairy desserts|red|1/2 cup|130|7|15|3
			Other desserts|red|2 oz|220|11|30|2
			Soda|red|8 oz|100|0|26|0""".split("\n")
			for i in range(len(s)):
				s[i] = s[i].strip().split("|")
				nft = models.FoodType(food_name=s[i][0], color=s[i][1],
				serv_name=s[i][2], calories=int(s[i][3]), fat_amt=int(s[i][4]),
				carb_amt=int(s[i][5]), protein_amt=int(s[i][6]))
				nft.uid = current_user.uid
				db.session.add(nft)
			db.session.commit()
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
		feq = models.Meal.query.filter(models.Meal.ts_created > timediff,
		models.Meal.uid==current_user.username).all()
		print(feq, file=sys.stderr)
		print(current_user.username, file=sys.stderr)
	else:
		feq = models.Meal.query.filter_by(uid="Guest").all()
		print("Guest", file=sys.stderr)
	feqd = {}
	for item in feq:
		feqd[item] = {"timestamp": datetime.datetime.utcfromtimestamp(models.Meal.ts_created).strf("%a, %B %d %Y, %M:%S")}
		print(item.elements, file=sys.stderr)
		feqd[item]['list'] = item.elements
	return render_template("stats.html", title="Stats", foodelems=feqd)

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
	u = models.User(username=data['username'], email=data['email'])
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
		return redirect("/signuporin")
	elif u.check_password(request.form['password']):
		login_user(u, remember=True)
		return redirect("/home")
	else:
		return redirect("/signuporin")

@app.route("/addfood", methods=["POST"])
def addfood():
	data = request.get_json()
	m = models.Meal(ts_created=int(datetime.datetime.utcnow().timestamp()), uid=current_user.username)
	db.session.add(m)
	db.session.commit()
	l = []
	for i in data:
		print(i, file=sys.stderr)
		fe = models.FoodElement(fid=i['id'], sid=i['serving'], uid=i['username'], mealid=m.mid, calories=i['calories'],
		protein_amt=i['protein'], fat_amt=i['fat'], carb_amt=i['carbs'], previous_changes=False, food_name=i['name'])
		l.append(fe)
		db.session.add(fe)
	db.session.commit()
	return ""

