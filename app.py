import sqlite3
from flask import Flask, g, render_template, session, redirect, url_for, request, flash, abort, jsonify

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

@app.route('/')
def index():
    db = get_db()
    query = db.execute('select * from posts order by id desc')
    posts = query.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Successfully logged in')
            return redirect(url_for('index'))
    return render_template('index.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Successfully logged out')
    return redirect(url_for('index'))

@app.route('/posts', methods=['POST'])
def create():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute(
        'insert into posts (title, body) values (?, ?)',
        [request.form['title'], request.form['body']]
    )
    db.commit()
    flash('Successfully created new post')
    return redirect(url_for('index'))

@app.route('/delete/<post_id>', methods=['GET'])
def delete(post_id):
    result = {'status': 0, 'message': 'Error'}
    try:
        db = get_db()
        db.execute('delete from posts where id=' + post_id)
        db.commit()
        result = {'status': 1, 'message': 'Post deleted'}
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run()