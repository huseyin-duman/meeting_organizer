import sqlite3
from datetime import datetime
connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())