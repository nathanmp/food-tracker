from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class FoodType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	food_name = db.Column(db.String(64))
	serv_name = db.Column(db.String(64))
	protein_amt = db.Column(db.Integer())
	carb_amt = db.Column(db.Integer())
	fat_amt = db.Column(db.Integer())
	def __repr__(self):
		return ("<FoodType Number {}, Name {}, SS {}>").format(self.id, self.food_name, self.serv_name)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(128), unique=True)
	password_hash = db.Column(db.String(128), unique=True)
	food_types = db.Column(db.String(400))
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.foreign_key('user.id'))
	str_rep = db.Column(db.String(400))
	timestamp = db.Column(db.Integer, default=datetime.utcnow)
