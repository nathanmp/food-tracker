from datetime import datetime
from flask import Flask, request, render_template
from flask_login import LoginManager, current_user, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3
import json
import sys
import os
from eatr import db
from werkzeug.security import generate_password_hash, check_password_hash

meals = db.Table("meals",
	db.Column("mealid", db.Integer, db.ForeignKey("meal.mid"), primary_key=True),
	db.Column("userid", db.Integer, db.ForeignKey("user.uid"), primary_key=True)
)
class FoodType(db.Model):
	def __repr__(self):
		return ("<FoodType Number {}, Name {}, SS {}>").format(self.ftid, self.food_name, self.serv_name)
	__tablename__ = "foodtype"
	ftid = db.Column(db.Integer, primary_key=True)
	food_name = db.Column(db.String(64))
	color = db.Column(db.String(10))
	serv_name = db.Column(db.String(64))
	protein_amt = db.Column(db.Integer())
	carb_amt = db.Column(db.Integer())
	fat_amt = db.Column(db.Integer())
	calories = db.Column(db.Integer())
	uid = db.Column(db.Integer, db.ForeignKey("user.uid"))

class User(UserMixin, db.Model):
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def get_id(self):
		return self.username
	def __repr__(self):
		return ("<UserID {}, Username {}, Email {}>").format(self.uid, self.username, self.email)
	
	__tablename__ = "user"
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(128), unique=True)
	password_hash = db.Column(db.String(128))
	foodtypes = db.relationship(FoodType, backref="user")
	meals = db.relationship("Meal", secondary=meals, lazy="subquery", backref="user")
	
class FoodElement(db.Model):
	def __repr__(self):
		ft = FoodType.query.filter_by(ftid=self.fid).first()
		return ("<FoodElement, FID {}, Username {}, SS {}, Time {}>").format(ft.food_name, self.uid, self.sid, self.timestamp)
	
	__tablename__ = "foodelement"
	eid = db.Column(db.Integer, primary_key=True)
	fid = db.Column(db.Integer, db.ForeignKey('foodtype.ftid'))
	sid = db.Column(db.Float)
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	color = db.Column(db.String(10))
	timestamp = db.Column(db.Integer, default=datetime.utcnow())
	carb_amt = db.Column(db.Integer)
	protein_amt = db.Column(db.Integer)
	fat_amt = db.Column(db.Integer)
	calories = db.Column(db.Integer)
	food_name = db.Column(db.String(64))
	previous_changes = db.Column(db.Boolean())
	mealid = db.Column(db.Integer, db.ForeignKey("meal.mid"))

class Meal(db.Model):
	__tablename__ = "meal"
	mid = db.Column(db.Integer, primary_key=True)
	elements = db.relationship('FoodElement', backref="meal", lazy=True)
	ts_created = db.Column(db.Integer)
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
