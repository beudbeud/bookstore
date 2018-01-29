import os
from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy

DATA_FOLDER = '/tmp/bookstore/'
UPLOAD_FOLDER = DATA_FOLDER + 'upload'
DB_FOLDER = DATA_FOLDER + 'db'
ALLOWED_EXTENSIONS = set(['epub'])
COVER_SIZE = 300

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s/test.db' % DB_FOLDER
app.secret_key = 'super secret key'
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COVER_SIZE'] = COVER_SIZE

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

if not os.path.exists(DATA_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    os.makedirs(DB_FOLDER)

