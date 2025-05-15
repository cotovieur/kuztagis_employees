# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workers')
def workers():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workers')
    workers = cursor.fetchall()
    conn.close()
    return render_template('workers.html', workers=workers)

@app.route('/items')
def items():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT i.item_id, i.name, i.is_specialty, COUNT(wi.worker_id) as worker_count
    FROM items i
    LEFT JOIN worker_item wi ON i.item_id = wi.item_id
    GROUP BY i.item_id
    ''')
    items = cursor.fetchall()
    conn.close()
    return render_template('items.html', items=items)

@app.route('/assign')
def assign():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workers')
    workers = cursor.fetchall()
    cursor.execute('''
    SELECT i.item_id, i.name, i.is_specialty, COUNT(wi.worker_id) as worker_count
    FROM items i
    LEFT JOIN worker_item wi ON i.item_id = wi.item_id
    GROUP BY i.item_id
    ''')
    items = cursor.fetchall()
    conn.close()
    return render_template('assign.html', workers=workers, items=items)

@app.route('/add_worker_to_item', methods=['POST'])
def add_worker_to_item():
    data = request.get_json()
    worker_id = data['worker_id']
    item_id = data['item_id']

    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO worker_item (worker_id, item_id) VALUES (?, ?)', (worker_id, item_id))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
