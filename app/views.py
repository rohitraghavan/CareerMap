from app import app, models, db
from .models import *
from flask import render_template, Flask, redirect, url_for, session, request, escape, g
#from flask_oauthlib.client import OAuth


@app.route("/")
@app.route("/index")
def index():
    '''
    Redirects to login screen if not logged in
    Displays course concentration selectors
    '''
    current_user = ""
    if "username" in session:
        current_user = escape(session["username"])
        return render_template("index.html", user=current_user)
    else:
        return redirect("login")


@app.route("/login")
def login():
    '''
    Displays login screen
    '''
    return render_template("login.html", login=True)


@app.route("/authenticate-login", methods=["POST"])
def authenticate_login():
    '''
    Authenticates login and redirects to index if sucessful
    Remove once Linkedin login is implemented
    '''
    if request.method == "POST":
        username = request.form["username"]
        if authenticate_user(username):
            session["username"] = username
            return redirect("index")
        else:
            return redirect("login")


def authenticate_user(username):
    '''
    Retrieves users from db to authenticate attempted login
    Remove once Linkedin login is implemented
    '''
    user_rows = models.retrieve_users()
    for user_row in user_rows:
        if user_row["user_id"] == username:
            return True
    return False


@app.route("/logout", methods=["GET", "POST"])
def logout():
    '''
    Logs the user out and redirects to login page
    '''
    session.pop("username")
    session.pop("concentration_name")
    return redirect("login")


@app.route("/select-concentration", methods=["POST"])
def select_concentration():
    '''
    Gets the selected concentration from the from and calls method to display
    a list of courses under the selected concentration
    '''
    if request.method == "POST":
        concentration_name = escape(request.form["concentration-name"])
        print(concentration_name)
        session["concentration_name"] = concentration_name
        return display_concentration_courses(concentration_name)


def display_concentration_courses(concentration_name):
    '''
    Displays a list of courses under the selected concentration
    '''
    current_user = escape(session["username"])
    courses = models.retrieve_courses(concentration_name)
    for course in courses:
        print(course["course_name"])
    return render_template("index.html", user=current_user, concentration_name=concentration_name, courses=courses)


@app.route("/add-course", methods=["POST"])
def add_course():
    '''
    Adds a course input by the user to the database
    '''
    if request.method == "POST":
        concentration_name = escape(session["concentration_name"])
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        instructor = request.form["instructor"]
        models.insert_course(concentration_name, course_id,
                             course_name, instructor)
        return display_concentration_courses(concentration_name)


@app.route("/add-rating", methods=["POST"])
def add_rating():
    '''
    Add a thumbs up by user to the database
    '''
    if request.method == "POST":
        concentration_name = escape(session["concentration_name"])
        user_id = escape(session["username"])
        course_ref = request.form["course_ref"]
        models.insert_rating(course_ref, user_id, concentration_name)
        return display_concentration_courses(concentration_name)


@app.route("/review/<value>")
def review(value):
    session['value'] = value
    get_course = models.retrieve_name(value)
    current_user = escape(session["username"])
    reviews = models.retrieve_review(value)
    return render_template("review.html", name=get_course[0], user=current_user, reviews=reviews, value=value)


@app.route("/review/add-review", methods=["GET", "POST"])
def add_review():
    '''
    Adds a review input by the user to the database
    '''
    value = session['value']
    if request.method == "POST":
        # concetration_name = request.form["concentration-name-add"]
        current_user = escape(session["username"])
        review = request.form["review"]
        models.insert_review(value, current_user, review)
    return redirect("review/{}".format(value))
