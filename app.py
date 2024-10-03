import sqlite3
conn = sqlite3.connect("shoppinglist.db")
c = conn.cursor()
#any interactive db update
conn.close()
