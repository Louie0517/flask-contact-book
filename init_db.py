import sqlite3 

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

cursor.execute(''' 
               CREATE TABLE IF NOT EXISTS owners 
               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
               username TEXT UNIQUE NOT NULL, 
               password TEXT UNIQUE NULL, 
               image TEXT) 
               ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS contacts 
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               phone TEXT NOT NULL,
               email TEXT NOT NULL,
               address TEXT NOT NULL,
               image TEXT)
               ''')

conn.commit()
conn.close()
print("Database initialized!")