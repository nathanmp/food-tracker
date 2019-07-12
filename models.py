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

class ExerciseType(db.Model):
	def __repr__(self):
		return ("<UserID {}, Name {}, METS {}>").format(self.uid, self.name, self.mets)
	__tablename__ = "exercisetype"
	tid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	mets = db.Column(db.Float)
	serv_name = db.Column(db.String(64))
	calories = db.Column(db.Integer)
	caloriesperweight = db.Column(db.Integer)
	uid = db.Column(db.Integer, db.ForeignKey("user.uid"))

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
	exercisetypes = db.relationship(ExerciseType)
	meals = db.relationship("DataSet", lazy="subquery", backref="user")

class FoodData(db.Model):
	def __repr__(self):
		ft = FoodType.query.filter_by(ftid=self.fid).first()
		return ("<FoodData, FID {}, Username {}, SS {}, Time {}>").format(ft.food_name, self.uid, self.sid, self.timestamp)
	
	__tablename__ = "foodelement"
	elementid = db.Column(db.Integer, primary_key=True)
	foodtypeid = db.Column(db.Integer, db.ForeignKey('foodtype.ftid'))
	servingsize = db.Column(db.Float)
	userid = db.Column(db.String(64), db.ForeignKey('user.username'))
	color = db.Column(db.String(10))
	timestamp = db.Column(db.Integer, default=datetime.utcnow())
	carb_amt = db.Column(db.Integer)
	protein_amt = db.Column(db.Integer)
	fat_amt = db.Column(db.Integer)
	calories = db.Column(db.Integer)
	food_name = db.Column(db.String(64))
	previous_changes = db.Column(db.Boolean())
	active = db.Column(db.Boolean(), default=True)
	mealid = db.Column(db.Integer, db.ForeignKey("meal.mid"))

class DataSet(db.Model):
	__tablename__ = "meal"
	mid = db.Column(db.Integer, primary_key=True)
	elements = db.relationship('FoodData', backref="meal", lazy=True)
	eelements = db.relationship('ExerciseData', backref="meal", lazy=True)
	ts_created = db.Column(db.Integer, default=datetime.utcnow())
	uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
	details = db.Column(db.String(300), default="")
	##represented in 100ths of a pound to prevent rounding issues
	weightval = db.Column(db.Integer)
	timeoffset = db.Column(db.Integer)

# ~ class WeightElement(db.Model):
	# ~ __tablename__ = "weightelement"
	# ~ weightid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# ~ ts_created = db.Column(db.Integer, default=datetime.timestamp(datetime.utcnow()))
	# ~ uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	# ~ mealid = db.Column(db.Integer, db.ForeignKey("meal.mid"))
	# ~ ##represented in 100ths of a pound to prevent rounding issues
"""
class Post(db.Model):
	__tablename__ = "post"
	pid = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(300))
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))

class Tag(db.Model):
	__tablename__ = "tag"
	tid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	posts = db.relationship("Post", secondary=tags, lazy=True, backref=db.backref("tags"))
"""
	
class ExerciseData(db.Model):
	__tablename__ = "exerciseelement"
	eid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
	ts_created = db.Column(db.Integer, default=datetime.timestamp(datetime.utcnow()))
	length = db.Column(db.Integer)
	etid = db.Column(db.Integer, db.ForeignKey('exercisetype.tid'))
	calsburned = db.Column(db.Integer)
	previous_changes = db.Column(db.Boolean())
	mealid = db.Column(db.Integer, db.ForeignKey("meal.mid"))
	active = db.Column(db.Boolean(), default=True)
	ename = db.Column(db.String(40))

class CalorieTarget(db.Model):
	__tablename__ = "calorietarget"
	ctid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	dtstarted = db.Column(db.String(40))
	dtended = db.Column(db.String(40))
	target = db.Column(db.Integer)
