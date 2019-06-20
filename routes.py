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
food_defaults_med = """Water|blue|1 cup|0|0|0|0
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

exercise_defaults_med = """Light exercise (<3 METs)|3|1 hour|3
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
	# ~ flist = current_user.foodtypes
	# ~ if flist == []:
		# ~ for i in range(len(food_defaults_med)):
			# ~ food_defaults_med[i] = food_defaults_med[i].strip().split("|")
			# ~ nft = models.FoodType(food_name=food_defaults_med[i][0], color=food_defaults_med[i][1],
			# ~ serv_name=food_defaults_med[i][2], calories=int(food_defaults_med[i][3]), fat_amt=int(food_defaults_med[i][4]),
			# ~ carb_amt=int(food_defaults_med[i][5]), protein_amt=int(food_defaults_med[i][6]))
			# ~ nft.uid = current_user.uid
			# ~ db.session.add(nft)
		# ~ db.session.commit()
		# ~ flist = current_user.foodtypes
	# ~ colors = []
	# ~ for i in flist:
		# ~ colors.append({"name":i.food_name, "id":i.ftid, "color":i.color, "serving":i.serv_name,
		# ~ "protein":i.protein_amt, "fat":i.fat_amt, "carbs":i.carb_amt, "calories":i.calories})
	# ~ postlist = []
	# ~ follows = current_user.follows
	# ~ print(str(follows), file=sys.stderr)
	# ~ return render_template("home.html", quickadd=colors)

@app.route("/addfood", methods=["GET"])
def addfoodpg():
	if current_user.is_anonymous:
		return redirect("/signuporin")
	else:
		flist = current_user.foodtypes
		if flist == []:
			for i in range(len(food_defaults_med)):
				food_defaults_med[i] = food_defaults_med[i].strip().split("|")
				
				nft = models.FoodType(food_name=food_defaults_med[i][0], color=food_defaults_med[i][1],
				serv_name=food_defaults_med[i][2], calories=int(food_defaults_med[i][3]), fat_amt=int(food_defaults_med[i][4]),
				carb_amt=int(food_defaults_med[i][5]), protein_amt=int(food_defaults_med[i][6]))
				
				nft.uid = current_user.uid
				db.session.add(nft)
			db.session.commit()
			flist = current_user.foodtypes
		colors = []
		for i in flist:
			colors.append({"name":i.food_name, "id":i.ftid, "color":i.color, "serving":i.serv_name,
				"protein":i.protein_amt, "fat":i.fat_amt, "carbs":i.carb_amt, "calories":i.calories})
		
		elist = current_user.exercisetypes
		if elist == []:
			for i in range(len(exercise_defaults_med)):
				exercise_defaults_med[i] = exercise_defaults_med[i].strip().split("|")
				print(exercise_defaults_med[i], file=sys.stderr)
				net = models.ExerciseType(name=exercise_defaults_med[i][0], mets=exercise_defaults_med[i][1],
				serv_name=exercise_defaults_med[i][2], calperlb=exercise_defaults_med[i][3])
				net.uid = current_user.uid
				db.session.add(net)
				elist.append(net)
			db.session.commit()
			elist = current_user.exercisetypes
		exercises = []
		for i in elist:
			print(i, file=sys.stderr)
			exercises.append({"name":i.name, "id":i.tid, "serving":i.serv_name, "mets":i.mets})
		
		return render_template("food-index.html", title="Home", foods=colors, elist=exercises, cuser=current_user)


@app.route("/addfood", methods=["POST"])
def addfood():
	data = request.get_json()
	m = models.Meal(ts_created=int(datetime.utcnow().timestamp()), uid=current_user.username, details=data['foods'][-1])
	db.session.add(m)
	db.session.commit()
	l = []
	for i in data["foods"][:-1]:
		print(i, file=sys.stderr)
		fe = models.FoodElement(fid=i['id'], sid=i['serving'], uid=i['username'], mealid=m.mid, calories=i['calories'],
		protein_amt=i['protein'], fat_amt=i['fat'], carb_amt=i['carbs'], previous_changes=False, food_name=i['name'], color=i['color'])
		db.session.add(fe)
	for i in data["exercises"]:
		print(i, file=sys.stderr)
		ee = models.ExerciseElement(uid=i['username'], mealid=m.mid, calsburned=i['calories'],
		previous_changes=False, ename=i['name'], length=i['length'])
		db.session.add(ee)
	db.session.commit()
	return ""

@app.route("/foodstats/", defaults={"timeframe":-1})
@app.route("/foodstats/<int:timeframe>")
def stats(timeframe):
	if timeframe == -1:
		tf = date.today() - date(2019, 6, 1)
		timeframe = tf.days
		timediff = datetime(2019, 6, 1)
		timediff = datetime.timestamp(timediff)
	else:
		timediff = datetime.utcnow() - timedelta(days=timeframe-1)
		timediff = datetime.timestamp(timediff)
	if current_user.is_authenticated:
		feq = models.Meal.query.filter(models.Meal.ts_created>timediff).filter_by(uid=current_user.username).all()
	else:
		feq = models.Meal.query.filter_by(uid="Guest").all()
	feqd = []
	ddict = {}
	td = date.today()
	ddict[td] = []
	timediff = timedelta(days=1)
	for i in range(timeframe):
		td = td - timediff
		print(td, file=sys.stderr)
		ddict[td] = []
	for item in feq:
		dt = datetime.utcfromtimestamp(item.ts_created)
		d = date.fromtimestamp(item.ts_created)
		feqd.append({"mealid": item.mid, "timestamp": dt.strftime("%B %d %Y, %I:%M%p"), "details":item.details})
		feqd[-1]['flist'] = []
		feqd[-1]['elist'] = []
		for i in item.elements:
			tempd = {"color":i.color, "name":i.food_name, "carb_amt":i.carb_amt, "fat_amt":i.fat_amt, "protein_amt":i.protein_amt, "calories":i.calories, "sid":i.sid, "active":i.active, "eid":i.eid}
			feqd[-1]['flist'].append(tempd)
			print(str(tempd), file=sys.stderr)
			ddict[d].append(tempd)
		for i in item.eelements:
			tempd = {"eid":i.eid, "uid":i.uid, "calories":i.calsburned, "previous_changes":False, "ename":i.ename, "length":i.length}
			print(str(tempd), file=sys.stderr)
			feqd[-1]['elist'].append(tempd)
			##ddict[d][1].append(tempd)
	nddict = {}
	print(ddict, file=sys.stderr)
	for k in ddict.keys():
		tdict = {"fat":0, "protein":0, "carbs":0, "calories":0}
		print(ddict[k], file=sys.stderr)
		for i in ddict[k]:
			if i['color'] not in tdict.keys():
				tdict[i['color']] = i['sid']
			else:
				tdict[i['color']] += i['sid']
			tdict['fat'] += i['fat_amt']
			tdict['protein'] += i['protein_amt']
			tdict['carbs'] += i['carb_amt']
			tdict['calories'] += i['calories']
		nddict[k.strftime("%B %d %Y")] = tdict
	
	print(str(nddict), file=sys.stderr)
	return render_template("stats.html", title="Stats", meals=feqd, d=nddict)

@app.route("/signup", methods=["GET"])
def signuppg():
	return render_template("signup.html")


@app.route("/signuporin", methods=["GET"])
def sorl():
	return render_template("signuporin.html")

@app.route("/deletemeal/", defaults={"mealid":-1})
@app.route("/deletemeal/<int:mealid>")
def deletemeal(mealid):
	if mealid == -1:
		return redirect('/foodstats')
	me = models.Meal.query.filter_by(mid=mealid).first()
	if me.uid == current_user.username:
		db.session.delete(me)
		db.session.commit()
	return redirect('/foodstats')

@app.route("/deletefood/", defaults={"foodid":-1})
@app.route("/deletefood/<int:foodid>")
def deletefood(foodid):
	if foodid == -1:
		return redirect('/foodstats')
	fe = models.FoodElement.query.filter_by(eid=foodid).first()
	print(fe.uid, file=sys.stderr)
	print(current_user.uid, file=sys.stderr)
	if str(fe.uid) == str(current_user.uid):
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

@app.route("/addweight", methods=["POST"])
def addweight():
	data = request.get_json()
	w = models.WeightElement(uid=current_user.username, ts_created=datetime.datetime.timestamp(datetime.utcnow()), val=int(data["weight"]))
	db.session.add(w)
	db.session.commit()
	return ""
