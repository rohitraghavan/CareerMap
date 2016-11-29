from app import app, models, db
from .models import *
from flask import render_template, Flask, redirect, url_for, session, request, jsonify, flash
#from flask_oauthlib.client import OAuth
# from .forms import LoginForm, SignUpForm, CareerForm


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html', login=True)


@app.route("/review")
def review():
    return render_template('review.html')


"""
app = Flask(__name__)
app.config.from_object('config')
oauth = OAuth()

linkedin = oauth.remote_app(
	'linkedIn',
	consumer_key='86faisvke7rqht',
	consumer_secret='vfywuq3lwEUUqzU2',
	request_token_params={
		'scope': 'r_basicprofile',
		'state': 'RandomString',
	},
	base_url='https://api.linkedin.com/v1/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
	authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)
# landing redirect
@myapp.route('/')
@myapp.route('/index')
def index():
	return redirect('/login')

# ------------ User Session Management ------------
# login
@myapp.route('/login', methods=['GET', 'POST'])
def login():
	user = ''
	error = None

	# if already logged in, redirect to the trips overview
	if 'user' in session:
		user = escape(session['user'])
		return redirect('/main')
	else: # login
		form = LoginForm()
		if form.validate_on_submit():
			error = None

			# user input
			email = form.email.data
			pwd = form.insecure_password.data

			# return user first name only if email, pwd match DB record
			user = models.validate_user(email, pwd)

			if user is not None:
				flash('Logging in')
				session['user'] = user
				session['email'] = email
				return redirect('/main')
			else:
				error = 'Invalid credentials'
	return render_template('login.html', error = error, form = form)

# sign up
@myapp.route('/signup', methods=['GET', 'POST'])
def signup():
	user = ''
	error = None

	# if already logged in, redirect to the trips overview
	if 'user' in session:
		user = escape(session['user'])
		return redirect('/trips')
	else: # sign up
		form = SignUpForm()
		if form.validate_on_submit():
			error = None

			# user input
			email = form.email.data
			pwd = form.insecure_password.data
			fname = form.fname.data
			lname = form.lname.data

			# insert the user into the database if the email address is not already associated with an account
			if models.retrieve_user_id(email) is None:
				user = models.signup_user(email, fname, lname, pwd)
				return redirect('/login')
			else:
				error = 'An account with that email address already exits.'
	return render_template('signup.html', error = error, form = form)

# logout
@myapp.route('/logout')
def logout():
	session.pop('user', None)
	flash('You were logged out')
	return redirect(url_for('login'))


@myapp.route('/main')
def main():
	if 'user' in session:
		form = CareerForm(request.form)
		user = escape(session['user'])
		if form.validate_on_submit():
			careers_name = form.careers_name.data
		return render_template('main.html', user = user, form=form)
	else: # login
		return redirect('/login')

@myapp.route('/select')
def select():
	if 'user' in session:
		user = escape(session['user'])
		return render_template('main2.html', user = user)
	else: # login
		return redirect('/login')
"""
