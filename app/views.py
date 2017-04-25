from app import app, models
from .models import *
from flask import render_template, Flask, redirect, url_for, session, request, escape


@app.route("/")
@app.route("/index")
def index():
    '''
    Redirects to login screen if not logged in
    Displays course concentration selectors
    '''
    current_user = ""
    if "user_id" in session:
        user_id = escape(session["user_id"])
        first_name = escape(session["first_name"])
        photo = escape(session["photo"])
        session["concentration_name"] = ""
        session.pop("concentration_name")
        return render_template("index.html", user=user_id, first_name=first_name, photo=photo)
    else:
        return redirect("login")


@app.route("/login")
def login():
    '''
    Displays login screen
    '''
    return render_template("login.html", login=True)

@app.route("/music", methods=['POST','GET'])
def music():
    '''
    Displays music search results
    '''
    print("HIIIIIIIIIIIIIIIIIIIIII")
    if request.method == "POST":
        typeofsearch = request.form["typeofsearch"]
        searchbox = request.form["searchbox"]
    print("BYEEEEEEEEEEEEEEEEEEE")
    return render_template("music.html", login=True)


@app.route("/rawdata", methods=['POST'])
def rawdata():
    '''
    Displays dataset 
    '''
    print("WORKING")
    return render_template("login.html", login=True)


@app.route("/authenticate-login", methods=["POST"])
def authenticate_login():
    '''
    Inserts linkedin login info to db and session and redirects to index page
    '''
    if request.method == "POST":
        user_id = request.form["user-id"]
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        photo = request.form["photo"]
        add_or_update_users(user_id, first_name, last_name, photo)
        session["user_id"] = user_id
        session["first_name"] = first_name
        session["photo"] = photo
        return redirect("index")


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
    first_name = escape(session["first_name"])
    photo = escape(session["photo"])
    courses = models.retrieve_courses(concentration_name)
    return render_template("index.html", concentration_name=concentration_name, courses=courses, first_name=first_name, photo=photo)


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
        user_id = escape(session["user_id"])
        course_ref = request.form["course_ref"]
        models.insert_rating(course_ref, user_id, concentration_name)
        return display_concentration_courses(concentration_name)


def display_reviews(course_ref, course_id, course_name):
    '''
    Displays reviews for the course
    '''
    first_name = escape(session["first_name"])
    photo = escape(session["photo"])
    reviews = models.retrieve_reviews(course_ref)
    return render_template("review.html", course_ref=course_ref, course_id=course_id, course_name=course_name, reviews=reviews, first_name=first_name, photo=photo)


# @app.route("/reviews", methods=["POST"])
# def reviews():
#     '''
#     Gets the course details from the form and calls method to display reviews
#     for that course
#     '''
#     if request.method == "POST":
#         course_ref = request.form["course_ref"]
#         course_id = request.form["course_id"]
#         course_name = request.form["course_name"]
#         reviews = models.retrieve_reviews(course_ref)
#         return display_reviews(course_ref, course_id, course_name)


@app.route("/add-review", methods=["GET", "POST"])
def add_review():
    '''
    Adds a review input by the user to the database
    '''
    if request.method == "POST":
        user_id = escape(session["user_id"])
        review = request.form["review"]
        course_ref = request.form["course_ref"]
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        models.insert_review(course_ref, user_id, review)
    return display_reviews(course_ref, course_id, course_name)
