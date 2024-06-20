from flask import Flask, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join('database', 'products.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    app.run()