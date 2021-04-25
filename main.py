import json
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from datetime import timedelta 
from datetime import datetime, date

from models import db, User, Medical
from forms import SignUp, LogIn

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
''' End Flask Login Functions '''

''' Begin boilerplate code '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7)
  CORS(app)
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here '''

def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

''' End JWT Setup '''

@app.route('/')
def home():
  return app.send_static_file('home.html')

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
      firstname=data['firstname'], lastname=data['lastname'], username=data['username'], email=data['email'],dob=data['dob'], address=data['address'])
    newuser.set_password(data['password'])
    db.session.add(newuser)
    db.session.commit()
    flash('Account Created!')
    return redirect(url_for('login'))
  flash('Error invalid input!')
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
#@jwt_required()
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('login')) 

@app.route('/checkup', methods=['POST'])
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
    blood_pressure= request.form.get('blood_pressure')
    )
  db.session.add(medical)
  db.session.commit()
  return redirect(url_for('medical'))

@app.route('/checkup', methods=['GET'])
def getcheck_up():
  return render_template('checkup.html')

@app.route('/medical', methods=['GET', 'POST'])
def medical():
  start = date(year=2021,month=1,day=1)
  today = date.today()
  end = today.strftime("%d/%m/%Y")
 
  medicals = Medical.query.filter(Medical.checkup <= end).filter(Medical.checkup >= start)
  return render_template('medical.html', medicals=medicals)

@app.route('/mymedical', methods=['GET'])
def mymedical():
  medicals = Medical.query.all()
  medicals = [medical.toDict() for medical in medicals]
  return json.dumps(medicals)

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users = [user.toDict() for user in users]
    return json.dumps(users)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)