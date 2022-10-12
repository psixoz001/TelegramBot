import sqlite3
from create_db import *

def findUser(user_id):
    return cursor.execute("SELECT id FROM users WHERE id=?",(user_id,)).fetchone()

def registration(user_id):
    cursor.execute("INSERT INTO users (id) VALUES(?)", (user_id,))

def findSubs(user_id):
   
    return cursor.execute("""SELECT categories.text FROM categories
    JOIN subscribes ON categories.id=subscribes.category_id
    JOIN users ON subscribes.user_id=users.id
    WHERE users.id=?""", (user_id,)).fetchall()

def subscribe(user_id,category_id):
    cursor.execute("INSERT INTO subscribes (user_id,category_id) VALUES(?,?)",(user_id,category_id,))
    connect.commit()

def unsubscribe(user_id,category_id):
    cursor.execute("DELETE FROM subscribes WHERE user_id=? and category_id=?", (user_id,category_id,))
    connect.commit()
def gimmeIdCategory(text):
    return cursor.execute("SELECT id FROM categories WHERE categories.text=?", (text,)).fetchone()

def findSubsAll(user_id,category_id):
    return cursor.execute("SELECT user_id FROM subscribes WHERE subscribes.user_id=? and subscribes.category_id=?", (user_id,category_id,)).fetchone()
