import sqlite3
from flask import Flask, render_template, g
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("shoppinglist.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

