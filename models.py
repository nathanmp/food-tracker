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

follows = db.Table("follows",
	db.Column("userid", db.Integer, db.ForeignKey("user.uid"), primary_key=True),
	db.Column("userid", db.Integer, db.ForeignKey("user.uid"), primary_key=True)
)

tags = db.Table("posttags",
	db.Column("pid", db.Integer, db.ForeignKey("post.pid"), primary_key=True),
	db.Column("tid", db.Integer, db.ForeignKey("tag.tid"), primary_key=True)
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
	follows = db.relationship("User", secondary=follows, lazy="dynamic", backref=db.backref('followers', lazy="dynamic"))
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
	active = db.Column(db.Boolean(), default=True)
	mealid = db.Column(db.Integer, db.ForeignKey("meal.mid"))
	follows = db.relationship("User", lazy=True)

class Meal(db.Model):
	__tablename__ = "meal"
	mid = db.Column(db.Integer, primary_key=True)
	elements = db.relationship('FoodElement', backref="meal", lazy=True)
	ts_created = db.Column(db.Integer)
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))

class WeightElement(db.Model):
	__tablename__ = "weightelement"
	wid = db.Column(db.Float, primary_key=True)
	ts_created = db.Column(db.Integer, default=datetime.timestamp(datetime.utcnow()))
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	val = db.Column(db.Float)

class Post(db.Model):
	__tablename__ = "post"
	pid = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(300))
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	tags = db.relationship("Tag", secondary=tags, backref=db.backref("post", lazy="joined"), lazy=True)

class Tag(db.Model):
	__tablename__ = "tag"
	tid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	posts = db.relationship("Post", secondary=tags, lazy=True)
	
class ExerciseType(db.Model):
	__tablename__ = "exercisetype"
	tid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	mets = db.Column(db.Float)
	color = db.Column(db.String(10))

class ExerciseElement(db.Model):
	__tablename__ = "exerciseelement"
	eid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
	ts_created = db.Column(db.Integer, default=datetime.timestamp(datetime.utcnow()))
	length = db.Column(db.Integer)
	etid = db.Column(db.Integer, db.ForeignKey('exercisetype.tid'))
	calsburned = db.Column(db.Integer)

class CalorieTarget(db.Model):
	__tablename__ = "calorietarget"
	ctid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	dtstarted = db.Column(db.String(40))
	dtended = db.Column(db.String(40))
	target = db.Column(db.Integer)
