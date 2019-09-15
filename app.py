import sqlite3
from flask import Flask, g

# configs
DATABASE = 'blog.db'
DEBUG = True
SECRET_KEY = 'secret_key'
USERNAME = 'admin'
PASSWORD = 'password'

# create and initialize
app = Flask(__name__)
app.config.from_object(__name__)

# connect to db
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# initialize db
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# open db connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# close db connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    init_db()
    app.run()