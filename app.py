import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug  import exceptions

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return 'Welcome home pal'

def getPosts(data):
    return {'id': data[0], 'date created': data[1],'title': data[2], 'post content': data[3]}

@app.route('/posts', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM posts').fetchall()
        postList = list(map(getPosts, posts))
        return jsonify(postList)

    if request.method == 'POST':
        data = request.json
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',(data['title'], data['post content']))
        conn.commit()
        return f'new post has been added'


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Opps... {err}"}), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_server_error(err):
    return jsonify({"message": f"{err} It's not you it's us. Press F to pay respect"})

if __name__=='__main__':
    app.run(debug=True)
