import sqlite3
from config import *
connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()
print("success")

def createDB():
    cursor.execute('''CREATE TABLE IF NOT EXISTS "users"("id" INTEGER UNIQUE);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "categories"(
            "id" INTEGER UNIQUE,
            "text" TEXT UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT));''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "subscribes"(
            "user_id" INTEGER ,
            "category_id" INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE);''')
    connect.commit()
    try:
        for key in category :
                cursor.execute("INSERT INTO categories(text) VALUES(?)", (key,))
                connect.commit()
    except: pass