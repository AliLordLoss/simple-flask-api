import sqlite3
import os


def init_db():
    connection = sqlite3.connect(os.environ.get('DB'))

    with open('init.sql') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()
