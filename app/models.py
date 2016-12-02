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
            "SELECT * FROM course_ratings_vw WHERE concentration_name = ? ORDER BY ratings DESC", (concentration_name,)).fetchall()
    return courses


def insert_course(concentration_name, course_id, course_name, instructor):
    '''
    Add course to the database under the concentration
    '''
    with sql.connect("career-map.db") as con:
        con.execute('pragma foreign_keys = ON')
        cur = con.cursor()
        # Check if course already exists in courses table.
        course_ref = cur.execute(
            "SELECT course_ref FROM courses WHERE course_id = ? AND course_name = ? AND instructor = ?",
            (course_id, course_name, instructor)).fetchone()
        # If course doesnt exist in db, insert it and fetch the course ref of
        # the newly inserted course
        if course_ref is None:
            # Course ref number increments automatically
            cur.execute("INSERT INTO courses (course_id, course_name, instructor) VALUES (?, ?, ?)",
                        (course_id, course_name, instructor))
            course_ref = cur.execute(
                "SELECT course_ref FROM courses WHERE course_id = ? AND course_name = ? AND instructor = ?",
                (course_id, course_name, instructor)).fetchone()

        # Set the course under the concentration
        cur.execute("INSERT INTO courses_per_concentration (course_ref, concentration_name) VALUES (?, ?)",
                    (course_ref[0], concentration_name))
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


def insert_review(course_ref, user_id, review):
    '''
    Add review for the course to the database
    '''
    with sql.connect("career-map.db") as con:
        #con.execute('pragma foreign_keys = ON')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO course_reviews (course_ref, user_id, review_text) VALUES (?, ?, ?)", (course_ref, user_id, review))
        con.commit()


def retrieve_reviews(course_ref):
    '''
    Retrieves course reviews for course_ref passed in input
    '''
    with sql.connect("career-map.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        reviews = cur.execute(
            "SELECT * FROM course_reviews WHERE course_ref = ?", (course_ref, )).fetchall()
    return reviews
