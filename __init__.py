from flask import Flask, request, render_template
from flask_login import LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import connexion
import sqlite3
import json
import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = """REDACTED"""

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)

from eatr import routes, models
from eatr.models import *
@app.shell_context_processor
def make_shell_context():
    return {'db': db, "FoodType":FoodType, "User":User, "FoodElement":FoodElement}
