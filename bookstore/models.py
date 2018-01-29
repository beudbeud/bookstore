from settings import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(250))
    email = db.Column(db.String(50), unique=True, index=True)
    admin = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime)

    def __init__(self , username ,password , email, admin):
        self.username = username
        self.set_password(password)
        self.email = email
        self.admin = admin
        self.registered_on = datetime.utcnow()

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Book(db.Model):
    __tablename__ = "ibooks"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, index=True)
    title = db.Column(db.String(250))
    author = db.Column(db.String(250))
    registered_on = db.Column(db.DateTime)

    def __init__(self, filename, title, author):
        self.filename = filename
        self.title = title
        self.author = author
        self.registered_on = datetime.utcnow()

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Book %r>' % (self.title)

db.create_all()
db.session.commit()
