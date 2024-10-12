import sqlite3
from flask import Flask, render_template, g, request, flash, get_flashed_messages, url_for, redirect
import os
import bcrypt

app = Flask(__name__)
app.secret_key='9375dab_0909fcb'


#Opening database connection

def get_shoppinglist_db_connection():
    connection = sqlite3.connect("shoppinglist.db")
    db = connection.cursor()
    return db, connection

def get_users_db_connection():
    connection = sqlite3.connect("users.db")
    db = connection.cursor()
    return db, connection


#Password hashing

def hash_password():
    user_password = request.form.get("password")
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt) 
    return hashed_password   



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/shoppinglist", methods=["GET"])
def shoppinglist():
    return render_template("shoppinglist.html")

@app.route("/shoppingmate", methods=["GET"])
def shoppingmate():
    return render_template("shoppingmate.html")

@app.route("/signup",methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username") #Get username from form
    password = request.form.get("password") #Get password from form
    password_confirmation = request.form.get("passwordcheck") #Get the password confirmation
    db, connection = get_users_db_connection()

    if db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchone() is None and password == password_confirmation:
        hashed_password_bytestring = hash_password() #Get user password, hash it with adding salt, return it as hashed_password
        hashed_password = hashed_password_bytestring.decode('utf-8')
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, hashed_password])
        connection.commit()
        connection.close()
        flash('Registered successfully!', 'success')
        return redirect (url_for('login'))
    
    elif db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchone() is not None:
        flash('Username already exists, please try registering again, with a different username.', 'danger')
        return render_template("signup.html")

    elif password != password_confirmation:
        flash('The passwords did not match, please ensure, that you are entering the same password twice.', 'danger')
        return render_template("signup.html")
        #Add error message

