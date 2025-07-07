from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignUp, LogIn
from datetime import datetime
db = SQLAlchemy()

## Create a User Model
class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  firstname = db.Column(db.String(120))
  lastname = db.Column(db.String(120))
  address = db.Column(db.String(200))
  dateofbirth = db.Column(db.DateTime)
  medicals = db.relationship('Medical', backref='user', lazy=True)

  def toDict(self):
    return {
      "id": self.id,
      "firstname": self.firstname,
      "lastname": self.lastname,
      "username": self.username,
      "email": self.email,
      "address": self.address,
      'dateofbirth': self.dateofbirth.strftime("%d/%m/%Y") if self.dateofbirth else ""

    }
    
  #hashes the password parameter and stores it in the object
  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
  #Returns true if the parameter is equal to the object's password property
  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password, password)
    
  #To String method
  def __repr__(self):
    return '<User {}>'.format(self.username) 

## Create a Medical Model
class Medical(db.Model):
  __tablename__ = 'medical'

  id = db.Column(db.Integer, primary_key=True)
  height = db.Column(db.Integer)
  weight = db.Column(db.Integer)
  bmi = db.Column(db.String(100))
  bst_type = db.Column(db.String(100))
  bs_test = db.Column(db.Integer)
  blood_sugar = db.Column(db.String(100))
  bp_systolic = db.Column(db.Integer)
  bp_diastolic = db.Column(db.Integer)
  bp_pulse = db.Column(db.Integer)
  blood_pressure = db.Column(db.String(100))
  checkup = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def toDict(self):
    return{
      'id': self.id,
      'checkup': self.checkup.strftime("%d/%m/%Y") if self.checkup else "",
      'body': {
          'height': self.height,
          'weight': self.weight,
          'bmi': self.bmi
          },
      'blood_sugar': {
          'type': self.bst_type,
          'test': self.bs_test,
          'bs_result': self.blood_sugar
          },
      'blood_pressure': {
          'bp_systolic': self.bp_systolic,
          'bp_diastolic': self.bp_diastolic,
          'bp_pulse': self.bp_pulse,
          'bp_result': self.blood_pressure
          },
          
    }

