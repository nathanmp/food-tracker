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
from datetime import datetime, date, timedelta
from eatr import db, app, models
app = Flask('eatr')
app.debug = True
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
food_defaults = """Water|blue|1 cup|0|0|0|0
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
	
exercise_defaults = """Light exercise (<3 METs)|3|1 hour|3
Medium exercise (3-6 METs)|5|1 hour|5
Intense exercise (>6 METs)|7|1 hour|7""".split("\n")

@login_manager.user_loader
def load_user(user_id):
	u = models.User.query.filter_by(username=user_id).first()
	return u

@app.route("/")	
@app.route("/home")	
def home():
	if current_user.is_anonymous:
		return redirect("/signuporin")
	else:
		return redirect("/addfood")

@app.route("/addfood", methods=["GET"])
def addfoodpage():
	if current_user.is_anonymous:
		return redirect("/signuporin")
	else:
		foodlist = current_user.foodtypes
		if foodlist == []:
			for i in range(len(food_defaults)):
				food_defaults[i] = food_defaults[i].strip().split("|")
				
				newfoodtype = models.FoodType(food_name=food_defaults[i][0], color=food_defaults[i][1],
				serv_name=food_defaults[i][2], calories=int(food_defaults[i][3]), fat_amt=int(food_defaults[i][4]),
				carb_amt=int(food_defaults[i][5]), protein_amt=int(food_defaults[i][6]))
				
				newfoodtype.uid = current_user.uid
				db.session.add(newfoodtype)
			db.session.commit()
			foodlist = current_user.foodtypes
		colors = []
		for i in foodlist:
			colors.append({"name":i.food_name, "id":i.ftid, "color":i.color, "serving":i.serv_name,
				"protein":i.protein_amt, "fat":i.fat_amt, "carbs":i.carb_amt, "calories":i.calories})
		
		exerciselist = current_user.exercisetypes
		if exerciselist == []:
			for i in range(len(exercise_defaults)):
				exercise_defaults[i] = exercise_defaults[i].strip().split("|")
				print(exercise_defaults[i], file=sys.stderr)
				net = models.ExerciseType(name=exercise_defaults[i][0], mets=exercise_defaults[i][1],
				serv_name=exercise_defaults[i][2], caloriesperweight=exercise_defaults[i][3])
				net.uid = current_user.uid
				db.session.add(net)
				exerciselist.append(net)
			db.session.commit()
			exerciselist = current_user.exercisetypes
		exercises = []
		for i in exerciselist:
			print(i, file=sys.stderr)
			exercises.append({"name":i.name, "id":i.tid, "serving":i.serv_name, "mets":i.mets})
		
		return render_template("food-index.html", title="Home", foods=colors, exerciselist=exercises, cuser=current_user)


@app.route("/addfood", methods=["POST"])
def addfood():
	data = request.get_json()
	m = models.DataSet(ts_created=int(datetime.utcnow().timestamp()), uid=current_user.uid, details=data['post'], timeoffset=data['tz'])
	if data['weight'] != -1:
		m.weightval = 100*float(data['weight'])
	else:
		m.weightval = -1
	db.session.add(m)
	db.session.commit()
	l = []
	for i in data["foods"]:
		##print(i, file=sys.stderr)
		fe = models.FoodData(foodtypeid=i['id'], servingsize=i['serving'], userid=i['uid'], mealid=m.mid, calories=i['calories'],
		protein_amt=i['protein'], fat_amt=i['fat'], carb_amt=i['carbs'], previous_changes=False, food_name=i['name'], color=i['color'])
		db.session.add(fe)
		##print(i, file=sys.stderr)
		m.elements.append(fe)
	for i in data["exercises"]:
		##print(i, file=sys.stderr)
		ee = models.ExerciseData(userid=i['uid'], mealid=m.mid, calsburned=i['calories'],
		previous_changes=False, ename=i['name'], length=i['length'])
		db.session.add(ee)
	db.session.commit()
	return ""

@app.route("/foodstats/", defaults={"timeframe":-1})
@app.route("/foodstats/<int:timeframe>")
def stats(timeframe):
	daydict = {}
	
	if timeframe == -1:
		##Get all foods since July 1 2019
		tf = date.today() - date(2019, 7, 1)
		timeframe = tf.days
		timediff = datetime(2019, 7, 1)
		timediff = datetime.timestamp(timediff)
	else:
		##Get all foods in (timeframe) days
		timediff = datetime.utcnow() - timedelta(days=timeframe-1)
		timediff = datetime.timestamp(timediff)
	
	for i in range(timeframe+1):
		temptime = datetime.today() - timedelta(days=i)
		print(temptime.strftime('%b %d %Y'), file=sys.stderr)
		daydict[temptime.strftime('%b %d %Y')] = {'fat':0, 'protein':0, 'carbs':0, 'calories':0}
	print(str(daydict), file=sys.stderr)
	if current_user.is_authenticated:
		meal_query = models.DataSet.query.filter(models.DataSet.ts_created>timediff).filter_by(uid=current_user.uid).all()
	else:
		meal_query = models.DataSet.query.filter_by(uid="Guest").all()
	
	data = []
	td = date.today()
	
	for item in meal_query:
		if item.timeoffset == None:
			item.timeoffset = 0
		##print(item, file=sys.stderr)
		data.append(item)

	for i in data:
		print("I: " + str(i), file=sys.stderr)
		for j in i.elements:
			print("J: " + str(j), file=sys.stderr)
			daydict[date.fromtimestamp(i.ts_created).strftime('%b %d %Y')]['fat'] += j.fat_amt
			daydict[date.fromtimestamp(i.ts_created).strftime('%b %d %Y')]['protein'] += j.protein_amt
			daydict[date.fromtimestamp(i.ts_created).strftime('%b %d %Y')]['carbs'] += j.carb_amt
			daydict[date.fromtimestamp(i.ts_created).strftime('%b %d %Y')]['calories'] += j.calories
	return render_template("stats.html", title="Stats", meals=data, d=daydict)

@app.route("/editfoods", methods=["GET"])
def editfoodspg():
	foodlist = current_user.foodtypes
	colors = []
	for i in foodlist:
		colors.append({"name":i.food_name, "id":i.ftid, "color":i.color, "servingsize":i.serv_name,
			"protein":i.protein_amt, "fat":i.fat_amt, "carbs":i.carb_amt, "calories":i.calories, "id":i.ftid})
	return render_template('edit-foods.html', foods=colors)
	
@app.route("/editfoodtypes", methods=["POST"])
def editfoods():
	print(str(data), file=sys.stderr)
	foodtype_query = models.FoodType.query.filter_by(uid=current_user.uid)
	for e in data:
		items = foodtype_query.filter_by(ftid=int(e['id'])).all()
		
		if int(e['id']) < 0 or len(items) == 0:
			i = models.FoodType()
		else:
			i = items[0]
			
		if e['delete'] == "on" and len(items) != 0:
			db.session.delete(i)
			continue
		
		i.food_name = e['name']
		i.uid = current_user.uid
		i.calories = int(e['calories'])
		i.fat_amt = int(e['fat'])
		i.protein_amt = int(e['protein'])
		i.carb_amt = int(e['carbs'])
		i.serv_name = e['serving']
		i.color = e['color']
		
		db.session.add(i)
	db.session.commit()
	return ""
@app.route("/signup", methods=["GET"])
def signuppg():
	return render_template("signup.html")

@app.route("/signuporin", methods=["GET"])
def sorl():
	return render_template("signuporin.html")

@app.route("/deletemeal", defaults={"mealid":-1})
@app.route("/deletemeal/<int:mealid>")
def deletemeal(mealid):
	print("MEALID: " + str(mealid), file=sys.stderr)
	if mealid == -1:
		return redirect('/foodstats')
	me = models.DataSet.query.filter_by(mid=mealid)
	print("MEALS: " + str(me), file=sys.stderr)
	me = me.first()
	print("MEAL: " + str(me), file=sys.stderr)
	if me.uid == current_user.uid:
		db.session.delete(me)
		db.session.commit()
	return redirect('/foodstats')

@app.route("/deletefood", methods=['POST'])
def deletefood():
	data = request.get_json()
	fe = models.FoodData.query.filter_by(elementid=data['id']).first()
	if str(fe.userid) == str(current_user.uid):
		print("Deleting", file=sys.stderr)
		db.session.delete(fe)
		db.session.commit()
	return redirect('/foodstats')

@app.route("/logout")
def logout():
	logout_user()
	return redirect("/")
	

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
	return redirect("/")

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
		return redirect("/")
	else:
		return redirect("/signuporin")

@app.template_filter("formattime")
def _jinja2_filter_datetime(value):
	return datetime.fromtimestamp(value).strftime('%b %d %Y %I:%M:%S %p')

@app.route("/editonefood", methods=["POST"])
def editonefood():
	data = request.get_json()
	val = models.FoodData.query.filter_by(elementid=data['id']).first()
	db.session.add(val)
	val.food_name = data['name']
	val.uid = current_user.uid
	val.calories = int(data['calories'])
	val.fat_amt = int(data['fat'])
	val.protein_amt = int(data['protein'])
	val.carb_amt = int(data['carbs'])
	val.serv_name = float(data['serving'])
	val.color = data['color']
	db.session.commit()
	return ""
