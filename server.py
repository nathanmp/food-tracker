from flask import Flask, request, render_template
from flask_login import current_user, login_user
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3
import json
import sys

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
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
def addfood():
    return render_template("food.html", title="Home", foods=colors)

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
	return 0

@app.route("/add", methods=["POST"])
def add():
	##dataDict = json.loads(data)
	print(request.get_json(), file=sys.stderr)
	return render_template("food.html", title="Home", foods=colors)
