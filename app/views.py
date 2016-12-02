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
        session["concentration_name"] = ""
        session.pop("concentration_name")
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


@app.route("/logout")
def logout():
    '''
    Logs the user out and redirects to login page
    '''
    session.pop("username")
    session["concentration_name"] = ""
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
        session["concentration_name"] = concentration_name
        return display_concentration_courses(concentration_name)


def display_concentration_courses(concentration_name):
    '''
    Displays a list of courses under the selected concentration
    '''
    current_user = escape(session["username"])
    courses = models.retrieve_courses(concentration_name)
    return render_template("index.html", user=current_user, concentration_name=concentration_name, courses=courses)


@app.route("/add-course", methods=["POST"])
def add_course():
    '''
    Adds a course input by the user to the database
    '''
    if request.method == "POST":
        concentration_name = escape(session["concentration_name"])
        course_id = request.form["course_id_add"]
        course_name = request.form["course_name_add"]
        instructor = request.form["instructor_add"]
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


def display_reviews(course_ref, course_id, course_name):
    '''
    Displays reviews for the course
    '''
    current_user = escape(session["username"])
    reviews = models.retrieve_reviews(course_ref)
    return render_template("review.html", user=current_user, course_ref=course_ref, course_id=course_id, course_name=course_name, reviews=reviews)


@app.route("/reviews", methods=["POST"])
def reviews():
    if request.method == "POST":
        course_ref = request.form["course_ref"]
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        reviews = models.retrieve_reviews(course_ref)
        return display_reviews(course_ref, course_id, course_name)


@app.route("/add-review", methods=["GET", "POST"])
def add_review():
    '''
    Adds a review input by the user to the database
    '''
    if request.method == "POST":
        current_user = escape(session["username"])
        review = request.form["review"]
        course_ref = request.form["course_ref"]
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        models.insert_review(course_ref, current_user, review)
    return display_reviews(course_ref, course_id, course_name)
