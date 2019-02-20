import os
basedir = os.path.abspath(os.path.dirname(__file__))
SERVER_NAME = "localhost.com:5000"
SESSION_COOKIE_HTTPONLY = False
REMEMBER_COOKIE_HTTPONLY = False
SECRET_KEY = "REDACTED"
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
	
