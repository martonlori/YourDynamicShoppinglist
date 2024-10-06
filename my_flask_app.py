import sqlite3
from flask import Flask, render_template, g
import os

app = Flask(__name__)



def get_shoppinglist_db_connection():
    conn = sqlite3.connect("shoppinglist.db")
    conn.row_factory = sqlite3.Row
    return conn

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