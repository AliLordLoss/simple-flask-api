import sqlite3

connection = sqlite3.connect('database.sqlite')

with open('init.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
