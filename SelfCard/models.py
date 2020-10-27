from flask_login import UserMixin
from . import db
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

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
  #id = db.Column(GUID(), primary_key=True, default=str(uuid.uuid4()))
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  endpoint = db.Column(db.String(100), db.ForeignKey('Domain.endpoint'), nullable=False)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  button = db.Column(db.String(100), nullable=True)
  buttonAction = db.Column(db.String(100), nullable=True)

