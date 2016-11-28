from flask import render_template, redirect, request, session, redirect, url_for, escape, Flask
import sqlite3 as sql
import os.path

database = 'career-map.db' # Name of database

def connect_db():
    return sql.connect(database)

# Need to get some sort of user id from linkedin to populate db
def insert_userid(user_id):
    con = connect_db()
    con.execute('pragma foreign_keys = ON')
    cur = con.cursor() #associates sql connection, important because cursor allows us to execute sql statements
    cur.execute("INSERT INTO users (user_id) VALUES (?)",(user_id))
    con.commit()

def retrieve_course(concentration):
    # retrieve top 5 classes per concentration
    con = connect_db()
    con.execute('pragma foreign_keys = ON')
    cur = con.cursor()
    results = cur.execute("SELECT course_name FROM courses_per_concentration_vw WHERE concentration_name = concentration").fetchall()
    return results

def insert_course(course_id, course, instructor):
    # Users are able to recommend another course not in the list
    con = connect_db()
    con.execute('pragma foreign_keys = ON')
    cur = con.cursor()
    # Will course ref number increment automatically?
    cur.execute("INSERT INTO courses (course_id, course_name, instructor) VALUES (?, ?, ?)",(course_id, course, instructor))
    con.commit()

def insert_review(ref, user, review):
    # Insert user's review in table course_reviews
    con = connect_db()
    con.execute('pragma foreign_keys = ON')
    cur = con.cursor()
    cur.execute("INSERT INTO course_reviews (ref, user_id, review_text) VALUES (?, ?, ?)", (ref, user, review))
    con.commit()

# def retrieve_review():
    # display review retrieved from table course_review_vw


# def retrieve_rating():
    # Retrieve average rating from database



"""
def insert_data(company,email,phone,first_name,last_name,street_address,city,state,country,zip_code):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con: # giving connection a name 'con', 
        con.execute('pragma foreign_keys = ON')
        cur = con.cursor() #associates sql connection, importatnt because cursor allows us to execute sql statements
        cur.execute("INSERT INTO customers (company,email,phone,first_name,last_name) VALUES (?,?,?,?,?)",(company,email,phone,first_name,last_name)) #size will start increasing with more attributes/columns
        con.commit()
        new_cur = con.cursor()
        new_cur.execute("INSERT INTO address (street_address,city,state,country,zip_code,customer_id) VALUES (?,?,?,?,?,?)",(street_address,city,state,country,zip_code,cur.lastrowid))
        con.commit() 

def retrieve_customers():
    # SQL statement to query database goes here
    with sql.connect("app.db") as con:
        con.execute('pragma foreign_keys = ON')
        con.row_factory = sql.Row
        cur = con.cursor()
        result = cur.execute("select * from customers").fetchall()
    return result #convert all rows in dictionary format for every customer, e.g. Result['Company']

def retrieve_address():
    # SQL statement to query database goes here
    with sql.connect("app.db") as con:
        con.execute('pragma foreign_keys = ON')
        con.row_factory = sql.Row
        cur = con.cursor()
        result2 = cur.execute("select * from address").fetchall()
    return result2 #convert all rows in dictionary format for every customer, e.g. Result['Company']


##You might have additional functions to access the database
def insert_order(name_of_part,manufacturer_of_part,value):
    with sql.connect("app.db") as con: # giving connection a name 'con', 
        con.execute('pragma foreign_keys = ON')
        cur = con.cursor() 
        cur.execute("INSERT INTO orders (name_of_part,manufacturer_of_part) VALUES (?,?)",(name_of_part,manufacturer_of_part))
        con.commit()
        new_cur=con.cursor()
        new_cur.execute("INSERT INTO customer_order (customer_id, order_id) VALUES (?,?)",(value,cur.lastrowid))

def retrieve_order():
    with sql.connect("app.db") as con:
        con.execute('pragma foreign_keys = ON')
        con.row_factory = sql.Row
        cur = con.cursor()
        result3 = cur.execute("select * from orders").fetchall()
    return result3
    """