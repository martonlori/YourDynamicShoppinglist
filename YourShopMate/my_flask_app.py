import sqlite3
from flask import Flask, render_template, g, request, flash, get_flashed_messages, url_for, redirect, session, jsonify
import datetime
import bcrypt

app = Flask(__name__)
app.secret_key='9375dab_0909fcb'


#Opening database connection

def get_db_connection():
    connection = sqlite3.connect("YourShopMate.db")
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
        db, connection = get_db_connection()
        username_entered = request.form.get("username_login")
        username_in_db = (db.execute("SELECT username FROM users WHERE username = ?", [username_entered])).fetchone()

        if username_in_db is None:
            flash('Username does not exist.', 'warning')
            return render_template("login.html")
        
        else:
            password_entered = request.form.get("password_login").encode("utf-8")
            password_in_db_str = ((db.execute("SELECT password FROM users WHERE username = ?", [username_entered])).fetchone())
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
    db, connection = get_db_connection()
    user= (db.execute("SELECT users_id FROM users WHERE username=?", [session["username"]])).fetchone()
    
    if user is None:
        flash('Please log into your account.', 'warning')
        return redirect(url_for('login'))
    else:
        user_id = user[0]

    available_shoppinglist = (db.execute("SELECT * FROM shoppinglists WHERE owner_id=? ORDER BY creation_date DESC", [user_id])).fetchall()
    print(available_shoppinglist)
    if not available_shoppinglist:
        return render_template("homepage.html", shoppinglists=available_shoppinglist)
   
    no_items_raw = db.execute("SELECT shoppinglists.shoppinglists_id, COUNT(items.items_id) AS item_count FROM shoppinglists LEFT JOIN items ON shoppinglists.shoppinglists_id = items.list_id AND items.checked = 0 WHERE shoppinglists.owner_id = ? GROUP BY shoppinglists.shoppinglists_id", [user_id]).fetchall()
    print(no_items_raw)
    if no_items_raw is None:
        no_items_raw = 0

    no_items_dict = {item[0]: item[1] for item in no_items_raw}  # `item[0]` = list_id, `item[1]` = item_count
    
    return render_template("homepage.html", shoppinglists=available_shoppinglist, no_items=no_items_dict)


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        username = request.form.get("username_register") #Get username from register form
        password = request.form.get("password_register") #Get password from form
        password_confirmation = request.form.get("passwordcheck") #Get the password confirmation
        db, connection = get_db_connection()

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


@app.route("/openList/<int:listId>")
def viewList(listId):
    db, connection = get_db_connection()
    shoppinglist = (db.execute("SELECT * FROM shoppinglists WHERE shoppinglists_id=?", [listId])).fetchone()
    print(shoppinglist)

    items = db.execute("SELECT * FROM items WHERE list_id=?", [listId]).fetchall()
    print(items)

    if shoppinglist is None:
        return jsonify({"error": "List not found"}), 404
    
    list_name = shoppinglist[4]

    items_data = []
    for item in items:
        item_data = {
            "id": item[0],
            "name": item[4],
            "quantity": item[5],
            "checked": item[3]
        }
        items_data.append(item_data)

    return render_template("shoppinglist.html", items_data=items_data, list_name=list_name)

@app.route("/deleteList/<int:listId>", methods = ["DELETE"])
def deleteList(listId):
    try:
        db, connection = get_db_connection()
        db.execute("DELETE FROM shoppinglists WHERE shoppinglists_id=?", [listId])
        db.execute("DELETE FROM items WHERE list_id=?", [listId])
        connection.commit()
        connection.close()
        return jsonify({"message": "List deleted successfully"}), 201
    except Exception as error:
        print(f"Something went wrong: {error}")


@app.route("/createList", methods=["POST"])
def createList():
    listName = request.form.get("name")
    creation_date = datetime.datetime.now()
    formatted_creation_date = creation_date.strftime("%b %d")
    db, connection = get_db_connection()

    user= (db.execute("SELECT users_id FROM users WHERE username=?", [session["username"]])).fetchone()
    
    if user is None:
        flash('Please log into your account.', 'warning')
        return redirect(url_for('login'))
    else:
        user_id = user[0]

    db.execute("INSERT INTO shoppinglists (name,owner_id,creation_date) VALUES (?,?,?)", [listName, user_id, formatted_creation_date])
    connection.commit()
    connection.close()
    
    return jsonify({"message": "List created successfully"}), 201

@app.route("/addItem", methods=["POST"])
def addItem():
    db, connection = get_db_connection()

    user= (db.execute("SELECT users_id FROM users WHERE username=?", [session["username"]])).fetchone()
    
    if user is None:
        flash('Please log into your account.', 'warning')
        return redirect(url_for('login'))
    else:
        user_id = user[0]
        listId = request.form.get("listId")
        itemName = request.form.get("itemName")
        quantity = request.form.get("quantity")

    if not all([listId, itemName, quantity]):
        return jsonify({"error": "Missing data"}), 400
    
    
    db.execute("INSERT INTO items (list_id, creator_id, name, quantity) VALUES (?, ?, ?, ?)", [listId, user_id, itemName, quantity])
    connection.commit()
    connection.close()

    return jsonify({"message": "List created successfully"}), 201


@app.route("/toggleCheck/<int:items_id>", methods = ["PUT"])
def toggleCheck(items_id):
    db, connection = get_db_connection()

    try:

        db.execute("UPDATE items SET checked=1 WHERE items_id = ? AND checked = 0", [items_id])
        return jsonify({"message" : "Item checked."}), 201

    except:
        print("An error occurred.")
        return jsonify({"message" : "Error checking the item"}), 400
    
    finally:
        connection.commit()
        connection.close()

@app.route("/deleteItem/<int:items_id>", methods=["DELETE"])
def deleteItem(items_id):
    db, connection = get_db_connection()

    try:
        db.execute("DELETE FROM items WHERE items_id=?", [items_id])
        return jsonify({"message" : "Item deleted successfully"}), 201

    except:
        print("Error deleting the item.")
        return jsonify({"message" : "Error deleting the item" }), 400

    finally:
        connection.commit()
        connection.close()

@app.route("/editItem/<int:items_id>", methods={"PUT"})
def editItem(items_id):
    itemName = request.form.get('itemName')
    quantity = request.form.get('quantity')
    db, connection = get_db_connection()

    try:
        db.execute("UPDATE items SET name=?, quantity=? WHERE items_id=?", [itemName, quantity, items_id])
        return jsonify({"message" : "Item modified successfully."}), 201
    
    except:
        print("Error modifying the item")
        return jsonify({"message" : "Error modifying the item"}), 400
    
    finally:
        connection.commit()
        connection.close()