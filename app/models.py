import psycopg2 as sql
import os
import urllib.parse

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ.get(
    "DATABASE_URL", "postgres://rohitraghavan@localhost:5432/irateischool"))


def add_or_update_users(user_id, first_name, last_name, photo):
    '''
    Add or update linkedin users to the databse
    '''
    with sql.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as con:
        cur = con.cursor()
        # Check if user already exists in users table
        cur.execute("SELECT * FROM users where user_id = %s", (user_id, ))
        db_user_id = cur.fetchone()
        # If user doesnt exist in db, insert it. Else update existing record
        if db_user_id is None:
            cur.execute("INSERT INTO users (user_id, first_name, last_name, photo) VALUES (%s, %s, %s, %s)",
                        (user_id, first_name, last_name, photo))
        else:
            cur.execute("UPDATE users SET first_name=%s, last_name=%s, photo=%s WHERE user_id=%s",
                        (first_name, last_name, photo, user_id))


def retrieve_courses(concentration_name):
    '''
    Retreive courses under the concentration
    '''
    with sql.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM course_ratings_vw WHERE concentration_name = %s ORDER BY ratings DESC", (concentration_name,))
        courses = cur.fetchall()
    return courses


def insert_course(concentration_name, course_id, course_name, instructor):
    '''
    Add course to the database under the concentration
    '''
    try:
        with sql.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as con:
            cur = con.cursor()
            # Check if course already exists in courses table.
            cur.execute(
                "SELECT course_ref FROM courses WHERE course_id = %s AND course_name = %s AND instructor = %s",
                (course_id, course_name, instructor))
            course_ref = cur.fetchone()
            # If course doesnt exist in db, insert it and fetch the course ref of
            # the newly inserted course
            if course_ref is None:
                # Course ref number increments automatically
                cur.execute("INSERT INTO courses (course_id, course_name, instructor) VALUES (%s, %s, %s)",
                            (course_id, course_name, instructor))
                cur.execute(
                    "SELECT course_ref FROM courses WHERE course_id = %s AND course_name = %s AND instructor = %s",
                    (course_id, course_name, instructor))
                course_ref = cur.fetchone()

            # Set the course under the concentration
            cur.execute("INSERT INTO courses_per_concentration (course_ref, concentration_name) VALUES (%s, %s)",
                        (course_ref[0], concentration_name))
            con.commit()
    except:
        con.close()


def insert_rating(course_ref, user_id, concentration_name):
    '''
    Add rating for the course to the database
    '''
    try:
        with sql.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO course_ratings (course_ref, user_id, concentration_name) VALUES (%s, %s, %s)", (course_ref, user_id, concentration_name))
            con.commit()
    except:
        con.close()


def insert_review(course_ref, user_id, review):
    '''
    Add review for the course to the database
    '''
    try:
        with sql.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO course_reviews (course_ref, user_id, review_text) VALUES (%s, %s, %s)", (course_ref, user_id, review))
            con.commit()
    except:
        con.close()


def retrieve_reviews(course_ref):
    '''
    Retrieves course reviews for course_ref passed in input
    '''
    with sql.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM course_reviews_vw WHERE course_ref = %s", (course_ref, ))
        reviews = cur.fetchall()
    return reviews
