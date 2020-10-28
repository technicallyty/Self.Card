from flask_login import UserMixin
from . import db
from sqlalchemy.types import TypeDecorator, CHAR

class User(UserMixin ,db.Model):
  __tablename__='User'
  id = db.Column(db.Integer, primary_key=True)  # primary keys required by SQLAlchemy
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  name = db.Column(db.String(1000), nullable=False)
  domains = db.relationship('Domain', backref='User', lazy=True)


class Domain(db.Model):
  __tablename__ = 'Domain'
  owner = db.Column(db.String(100), db.ForeignKey('User.email'), nullable=False) 
  endpoint = db.Column(db.String(100), unique=True, primary_key=True) 
  component = db.relationship('Components', backref='Domain', lazy=True)


class Components(db.Model):
  __tablename__='Components'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  endpoint = db.Column(db.String(100), db.ForeignKey('Domain.endpoint'), nullable=False)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  button = db.Column(db.String(100), nullable=True)
  buttonAction = db.Column(db.String(100), nullable=True)

