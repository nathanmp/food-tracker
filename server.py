from flask import Flask
from flask import render_template
from flask_login import current_user, login_user
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
colors = [{"name": "Green and cruciferous vegetables", "color": "green", "serv": "1 cup", "id":"1"},
		{"name": "Root vegetables and gourds", "color": "green", "serv": "1 cup", "id":"1"},
		{"name": "Berries and stone fruit", "color": "green", "serv": "1/2 cup", "id":"1"},
		{"name": "Apples, oranges, and pears", "color": "green", "serv": "1", "id":"1"},
		{"name": "Beans", "color": "yellow", "serv": "1/2 cup", "id":"1"},
		{"name": "Nuts", "color": "yellow", "serv": "1/2 oz", "id":"1"},
		{"name": "Poultry", "color": "yellow", "serv": "3 oz", "id":"1"},
		{"name": "Seafood", "color": "yellow", "serv": "3 oz", "id":"1"},
		{"name": "Red meat", "color": "red", "serv": "3 oz", "id":"1"},
		{"name": "Deli meat", "color": "red", "serv": "2 oz", "id":"1"},
		{"name": "Eggs", "color": "yellow", "serv": "1", "id":"1"},
		{"name": "Cheese", "color": "yellow", "serv": "1/4 cup", "id":"1"},
		{"name": "Yogurt", "color": "yellow", "serv": "1 cup", "id":"1"},
		{"name": "Milk", "color": "yellow", "serv": "1 cup", "id":"1"},
		{"name": "Wheat", "color": "yellow", "serv": "1 cup", "id":"1"},
		{"name": "Oils", "color": "red", "serv": "2 tbsp", "id":"1"},
		{"name": "Heavy sauces", "color": "red", "serv": "2 tbsp", "id":"1"},
		{"name": "Light sauces", "color": "yellow", "serv": "2 tbsp", "id":"1"},
		{"name": "Bread", "color": "yellow", "serv": "1 slice", "id":"1"},
		{"name": "Grains", "color": "yellow", "serv": "1 cup", "id":"1"},
		{"name": "Desserts", "color": "red", "serv": "1 oz", "id":"1"}]

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
	##add a meal code here
	return 0
