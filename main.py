import json
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from datetime import timedelta 
from datetime import datetime, date

from models import db, User, Medical
from forms import SignUp, LogIn

''' Begin Flask Login Functions '''
login_manager = LoginManager()
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
''' End Flask Login Functions '''

''' Begin boilerplate code '''

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__, static_url_path='')

    # Configuration with environment variables
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///instance/test.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv('SECRET_KEY', 'changeme'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'changeme'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=7),
    )

    CORS(app)
    login_manager.init_app(app)
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()

jwt = JWTManager(app)

''' End Boilerplate Code '''

''' Set up JWT here '''

#def authenticate(uname, password):
#  user = User.query.filter_by(username=uname).first()
#  if user and user.check_password(password):
#    return user

#def identity(payload):
#  return User.query.get(payload['identity'])


''' End JWT Setup '''

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp()
  return render_template('signup.html', form=form)

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp()
  if form.validate_on_submit():
    data = request.form 
    newuser = User(
            firstname     = form.firstname.data,
            lastname      = form.lastname.data,
            username      = form.username.data,
            email         = form.email.data,
            dateofbirth   = form.dob.data,        # ← match your model
            address       = form.address.data
        )
    newuser.set_password(data['password'])
    db.session.add(newuser)
    db.session.commit()
    flash('Account Created!')
    return redirect(url_for('login'))
  flash('Invalid input')
  return redirect(url_for('signup')) 

@app.route('/login', methods=['GET'])
def login():
  form = LogIn()
  return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit():
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']):
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('home'))
  flash('Invalid credentials')
  return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('login')) 

@app.route('/checkup', methods=['POST'])
@login_required
def check_up():
  cdate= request.form.get('checkup')

  medical = Medical(
    checkup = datetime.strptime(cdate, "%Y-%m-%d").date(),
    height= request.form.get('height'), 
    weight= request.form.get('weight'), 
    bmi= request.form.get('bmi'), 
    bst_type= request.form.get('bst_type'), 
    bs_test= request.form.get('bs_test'), 
    blood_sugar= request.form.get('blood_sugar'), 
    bp_systolic= request.form.get('bp_systolic'), 
    bp_diastolic= request.form.get('bp_diastolic'), 
    bp_pulse= request.form.get('bp_pulse'), 
    blood_pressure= request.form.get('blood_pressure'),
    user_id = current_user.id  # Link to the logged-in user
    )
  db.session.add(medical)
  db.session.commit()
  return redirect(url_for('medical'))

@app.route('/checkup', methods=['GET'])
@login_required
def getcheck_up():
  return render_template('checkup.html')

@app.route('/medical', methods=['GET', 'POST'])
@login_required
def medical():
  # set your date bounds
  start = date(2021, 1, 1)
  today    = date.today()

  # build and execute the query
  medicals = Medical.query.filter_by(user_id=current_user.id)\
        .filter(Medical.checkup >= start)\
        .filter(Medical.checkup <= today)\
        .all()

  # render the template
  return render_template('medical.html', medicals=medicals)

@app.route('/mymedical', methods=['GET'])
@login_required
def mymedical():
  medicals = Medical.query.filter_by(user_id=current_user.id).all()
  medicals = [medical.toDict() for medical in medicals]
  return json.dumps(medicals)

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users = [user.toDict() for user in users]
    return json.dumps(users)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081, debug=True)