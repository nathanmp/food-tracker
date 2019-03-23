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

class FoodType(db.Model):
	def __init__(self, ftid, color, serv, name, cal, fat, carb, pro):
		self.ftid = ftid
		self.color = color
		self.serv_name = serv
		self.food_name = name
		self.calories = cal
		self.carb_amt = carb
		self.protein_amt = pro
		self.fat_amt = fat
	__tablename__ = "foodtype"
	ftid = db.Column(db.Integer, primary_key=True)
	food_name = db.Column(db.String(64))
	color = db.Column(db.String(10))
	serv_name = db.Column(db.String(64))
	protein_amt = db.Column(db.Integer())
	carb_amt = db.Column(db.Integer())
	fat_amt = db.Column(db.Integer())
	calories = db.Column(db.Integer())
	def __repr__(self):
		return ("<FoodType Number {}, Name {}, SS {}>").format(self.ftid, self.food_name, self.serv_name)

""" @login.user_loader
def load_user(id):
	return User.query.get(int(id)) """

class User(UserMixin, db.Model):
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __init__(self, uname, addr):
		self.username = uname
		self.email = addr
		##self.set_password(passwd)
	
	__tablename__ = "user"
	
	def get_id(self):
		return self.username
	def __repr__(self):
		return ("<UserID {}, Username {}, Email {}>").format(self.uid, self.username, self.email)
	
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(128), unique=True)
	password_hash = db.Column(db.String(128))
	food_types = db.Column(db.String(400))
	
class FoodElement(db.Model):
	def __init__(self, food_id, serving, username="Guest"):
		self.fid = food_id
		self.sid = serving	
		self.uid = username
		ft = FoodType.query.filter_by(ftid=self.fid).first()
		self.food_name = ft.food_name
		self.color = ft.color
		self.calories = ft.calories
		self.carb_amt = ft.carb_amt
		self.protein_amt = ft.protein_amt
		self.fat_amt = ft.fat_amt
		self.timestamp = datetime.utcnow()
	def __repr__(self):
		ft = FoodType.query.filter_by(ftid=self.fid).first()
		return ("<FoodElement, FID {}, Username {}, SS {}, Time {}>").format(ft.food_name, self.uid, self.sid, self.timestamp)
	eid = db.Column(db.Integer, primary_key=True)
	fid = db.Column(db.Integer, db.ForeignKey('foodtype.ftid'))
	sid = db.Column(db.Float)
	uid = db.Column(db.String(64), db.ForeignKey('user.username'))
	color = db.Column(db.String(10))
	timestamp = db.Column(db.Integer, default=datetime.utcnow)
	carb_amt = db.Column(db.Integer)
	protein_amt = db.Column(db.Integer)
	fat_amt = db.Column(db.Integer)
	calories = db.Column(db.Integer)
	food_name = db.Column(db.String(64))
