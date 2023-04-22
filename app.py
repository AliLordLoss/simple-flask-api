import sqlite3, os
from flask import Flask, request
from .utils import res, validate_data
from .init import init_db

init_db()

app = Flask(__name__)
DB = os.environ.get('DB')

@app.route("/", methods=['GET'])
def user_list():
    with sqlite3.connect(DB) as conn:
        query_result = conn.execute("""
            SELECT json_group_array( json_object('id', id, 'name', name, 'family_name', family_name, 'email', email, 'city', city) ) AS json_result FROM (SELECT * FROM users ORDER BY id)
        """).fetchall()
        try:
            users = query_result[0][0]
        except IndexError:
            users = '[]'
    return res(users)


@app.route("/", methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        validate_data(data)
    except Exception as e:
        return res(str(e), 400)
    
    with sqlite3.connect(DB) as conn:
        user = conn.execute('INSERT INTO users (name, family_name, email, city) VALUES (?, ?, ?, ?)', (
            data['name'],
            data['family_name'],
            data['email'],
            data['city']
        ))
        conn.commit()

    return res(user)

@app.route('/<int:id>/', methods = ['GET'])
def get_user(id):
    with sqlite3.connect(DB) as conn:
        query_result = conn.execute("""
            SELECT json_object('id', id, 'name', name, 'family_name', family_name, 'email', email, 'city', city) FROM users WHERE id = ?
        """, (id, )).fetchall()
        try:
            user = query_result[0][0]
        except IndexError:
            return res('not found!', 404)
    return res(user)

@app.route('/<int:id>/', methods = ['PUT', 'PATCH'])
def update_user(id):
    data = request.get_json()
    try:
        validate_data(data)
    except Exception as e:
        return res(str(e), 400)
    
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            UPDATE users SET name = ?, family_name = ?, email = ?, city = ? WHERE id = ?
        """, (
            data['name'],
            data['family_name'],
            data['email'],
            data['city'],
            id
        )).fetchall()
    return get_user(id)

@app.route('/<int:id>/', methods = ['DELETE'])
def delete_user(id):
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            DELETE FROM users WHERE id = ?
        """, (id, ))
    return res()
