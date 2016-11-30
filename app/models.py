import sqlite3 as sql


def retrieve_users():
    '''
    Retrieves users from db
    Remove once Linkedin login is implemented
    '''
    with sql.connect("career-map.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        users = cur.execute("SELECT * FROM users").fetchall()
    return users


def retrieve_courses(concentration_name):
    '''
    Retreive courses under the concentration
    '''
    with sql.connect("career-map.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        courses = cur.execute(
            "SELECT * FROM course_ratings_vw WHERE concentration_name = '" + concentration_name + "' ORDER BY ratings DESC").fetchall()
    return courses

def retrieve_course_ref(concentration_name, course_id, course_name, instructor):
    '''
    Retreive course ref under the concentration
    '''
    with sql.connect("career-map.db") as con:
        con.execute('pragma foreign_keys = ON')
        con.row_factory = sql.Row
        cur = con.cursor()
        course_ref = cur.execute(
            "SELECT course_ref FROM courses WHERE course_id = '" + course_id + "' AND course_name = '" + course_name + "' AND instructor = '" + instructor + "'").fetchone()[0]
    return course_ref

def insert_course(concentration_name, course_id, course_name, instructor):
    '''
    Add course to the database under the concentration
    '''
    with sql.connect("career-map.db") as con:
        con.execute('pragma foreign_keys = ON')
        cur = con.cursor()
        # Course ref number increments automatically
        cur.execute("INSERT INTO courses (course_id, course_name, instructor) VALUES (?, ?, ?)",
                    (course_id, course_name, instructor))
        # Retreive course_ref for second insert into courses_per_concentration
        # table
        course_ref = cur.execute(
            "SELECT course_ref FROM courses WHERE course_id = '" + course_id + "' AND course_name = '" + course_name + "' AND instructor = '" + instructor + "'").fetchone()[0]
        cur.execute("INSERT INTO courses_per_concentration (course_ref, concentration_name) VALUES (?, ?)",
                    (course_ref, concentration_name))
        con.commit()

def insert_review(ref, user, review):
    '''
    Add review for the course to the database
    '''
    with sql.connect("career-map.db") as con:
        con.execute('pragma foreign_keys = ON')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO course_reviews (ref, user_id, review_text) VALUES (?, ?, ?)", (ref, user, review))
        con.commit()

def insert_rating(course_ref, user_id, concentration_name):
    '''
    Add rating for the course to the database
    '''
    print(course_ref, user_id, concentration_name)
    with sql.connect("career-map.db") as con:
        con.execute('pragma foreign_keys = ON')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO course_ratings (course_ref, user_id, concentration_name) VALUES (?, ?, ?)", (course_ref, user_id, concentration_name))
        con.commit()

# def retrieve_review():
    # display review retrieved from table course_review_vw


# def retrieve_rating():
    # Retrieve average rating from database