import sqlite3
from flask import Flask, render_template, g, request, flash, get_flashed_messages, url_for, redirect, session
import datetime
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
    user_password = request.form.get("password_register")
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt) 
    return hashed_password   



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/shoppingmate", methods=["GET"])
def shoppingmate():
    return render_template("shoppingmate.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        db, connection = get_users_db_connection()
        username_entered = request.form.get("username_login")
        username_in_db = (db.execute("SELECT username FROM users WHERE username = ?", [username_entered])).fetchone()

        if username_in_db is None:
            flash('Username does not exist.', 'warning')
            return render_template("login.html")
        
        else:
            password_entered = request.form.get("password_login").encode("utf-8")
            password_in_db_str = (db.execute("SELECT password FROM users WHERE username = ?", [username_entered])).fetchone()
            if password_in_db_str is None:
                flash('User not found', 'warning')
                return render_template("login.html")
            else:
                password_in_db = password_in_db_str[0].encode("utf-8")
                connection.commit()
                connection.close()
                
                if not bcrypt.checkpw(password_entered, password_in_db):
                    flash('Wrong password entered.', 'warning')
                    return render_template("login.html")
                else:
                    session["username"] = username_entered
                    flash('Login successful!', 'success')
                    return redirect(url_for('homepage'))
        
@app.route("/homepage", methods=["GET"])
def homepage():
    return render_template("homepage.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        username = request.form.get("username_register") #Get username from register form
        password = request.form.get("password_register") #Get password from form
        password_confirmation = request.form.get("passwordcheck") #Get the password confirmation
        db, connection = get_users_db_connection()

        if db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchone() is None and password == password_confirmation and username:
            hashed_password_bytestring = hash_password() #Get user password, hash it with adding salt, return it as hashed_password
            hashed_password = hashed_password_bytestring.decode('utf-8')
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, hashed_password])
            connection.commit()
            connection.close()
            flash('Registered successfully!', 'success')
            return redirect (url_for('login'))
        
        elif db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchone() is not None:
            flash('Username already exists, please try registering again, with a different username.', 'danger')
            return render_template("register.html")

        elif password != password_confirmation:
            flash('The passwords did not match, please ensure, that you are entering the same password twice.', 'danger')
            return render_template("register.html")
        
        elif not username:
            flash('Please enter a username to register!', 'danger')
            return render_template("register.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash('You are successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route("newlist", methods=["POST", "GET"])
def newlist():
#Set new_item dictionary, so every item has the following information
    new_item = {
        'name': '',
        'quantity': 0,
        'added_at': '',
        'status': 'unchecked',
        'added_by': ''
    }

    #From the html form, update these information, and commit to the database

    if request.method == "POST":
        if request.form.get("new_item_name") and request.form.get("new_item_quantity").isdigit():
            new_item["name"] = request.form.get("new_item_name")
            new_item["quantity"] = request.form.get("new_item_quantity")
            new_item["added_by"] = session["username"]
            new_item["added_at"] = datetime.datetime.now("%c")
            db, connection = get_shoppinglist_db_connection()
            db.execute("INSERT INTO shoppinglist (item_name, quantity, status, added_by, added_at) VALUES (?, ?, ?, ?, ?)", [new_item["name"], new_item["quantity"], new_item["status"], new_item["added_by"], new_item["added_at"]])
            connection.commit()
            connection.close()
        elif not request.form.get("new_item_name"):
            flash('Please specify the item.', 'danger')
            return render_template("shoppinglist.html")
        elif request.form.get("new_item_quantity").isdigit() == False:
            flash('Please enter a valid number for quantity.', 'danger')
    else:
        return render_template("shoppinglist.html")

        