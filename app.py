#app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from functools import wraps

# Load environment variables before creating the app
load_dotenv('secretkey.env')  # Explicitly specify the filename

app = Flask(__name__)

# Print the current working directory
print("Current Working Directory:", os.getcwd())
app.secret_key = os.getenv('SECRET_KEY')
# Debug print to check if the secret key is loaded
print("Secret Key:", app.secret_key)

# Load users from JSON file
def load_users():
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                return json.load(file)
    except json.JSONDecodeError:
        pass
    return {"users": []}

# Save users to JSON file
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

users_data = load_users()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Load users
        users = load_users()

        # Check if user exists and password is correct
        for user in users['users']:
            if user['username'] == username and check_password_hash(user['password'], password):
                session['username'] = username
                flash('You were successfully logged in!')
                return redirect(url_for('index'))

        flash('Invalid credentials!')
        return redirect(url_for('login'))

    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were successfully logged out!')
    return redirect(url_for('login'))

@app.route('/workers')
@login_required
def protected_workers():
    return f"Hello, {session['username']}! This is a protected page."
def workers():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workers')
    workers = cursor.fetchall()
    conn.close()
    return render_template('workers.html', workers=workers)

# Adding new worker
@app.route('/add', methods=['GET', 'POST'])
@login_required
def protected_add():
    return f"Hello, {session['username']}! This is a protected page."
def add_worker():
    if request.method == 'POST':
        worker_id = request.form['aisepo_id']
        fio = request.form['fio']
        position = request.form['position']
        education_level = request.form['education_level']
        specialty = request.form['specialty']
        qualification = request.form['qualification']
        academic_degree = request.form['academic_degree']
        academic_title = request.form['academic_title']
        professional_retraining = request.form['professional_retraining']
        total_experience = request.form['total_experience']
        specialty_experience = request.form['specialty_experience']
        courses = request.form['courses']

        conn = sqlite3.connect('workers.db')
        exists, message = check_worker_exists(conn, worker_id=worker_id, fio=fio)
        if exists:
            conn.close()
            return jsonify({'status': 'error', 'message': message}), 400

        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO workers (
            worker_id, fio, position, education_level, specialty, qualification,
            academic_degree, academic_title, professional_retraining,
            total_experience, specialty_experience, courses
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            worker_id, fio, position, education_level, specialty, qualification,
            academic_degree, academic_title, professional_retraining,
            total_experience, specialty_experience, courses
        ))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})

    return render_template('add_worker.html')

# Firing worker
@app.route('/fire', methods=['POST'])
def fire_worker():
    data = request.get_json()
    worker_id = data['worker_id']

    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    print(f"Firing worker_id: {worker_id}")  # Debug print
    cursor.execute('DELETE FROM workers WHERE worker_id = ?', (worker_id,))

    # Delete the worker from the worker_item table
    cursor.execute('DELETE FROM worker_item WHERE worker_id = ?', (worker_id,))

    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/get_worker')
def get_worker():
    worker_id = request.args.get('worker_id')
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workers WHERE worker_id = ?', (worker_id,))
    worker = cursor.fetchone()
    conn.close()

    if worker:
        return jsonify({
            'worker_id': worker[0],
            'fio': worker[1],
            'position': worker[2],
            'education_level': worker[3],
            'specialty': worker[4],
            'qualification': worker[5],
            'academic_degree': worker[6],
            'academic_title': worker[7],
            'professional_retraining': worker[8],
            'total_experience': worker[9],
            'specialty_experience': worker[10],
            'courses': worker[11]
        })
    else:
        return jsonify({'status': 'error', 'message': 'Worker not found'}), 404

# Checking if worker_id or fio is already recorded
def check_worker_exists(conn, worker_id=None, fio=None, exclude_worker_id=None):
    cursor = conn.cursor()

    if worker_id is not None:
        query = 'SELECT 1 FROM workers WHERE worker_id = ?'
        params = (worker_id,)
        if exclude_worker_id is not None:
            query += ' AND worker_id != ?'
            params += (exclude_worker_id,)
        cursor.execute(query, params)
        if cursor.fetchone():
            return True, "Worker ID already exists"

    if fio is not None:
        query = 'SELECT 1 FROM workers WHERE fio = ?'
        params = (fio,)
        if exclude_worker_id is not None:
            query += ' AND worker_id != ?'
            params += (exclude_worker_id,)
        cursor.execute(query, params)
        if cursor.fetchone():
            return True, "FIO already exists"

    return False, None

@app.route('/edit_worker', methods=['POST'])
def edit_worker():
    old_worker_id = request.form['old_worker_id']
    new_worker_id = request.form['worker_id']
    fio = request.form['fio']
    position = request.form['position']
    education_level = request.form['education_level']
    specialty = request.form['specialty']
    qualification = request.form['qualification']
    academic_degree = request.form['academic_degree']
    academic_title = request.form['academic_title']
    professional_retraining = request.form['professional_retraining']
    total_experience = request.form['total_experience']
    specialty_experience = request.form['specialty_experience']
    courses = request.form['courses']

    conn = sqlite3.connect('workers.db')
    exists, message = check_worker_exists(conn, worker_id=new_worker_id, fio=fio, exclude_worker_id=old_worker_id)
    if exists:
        conn.close()
        return jsonify({'status': 'error', 'message': message}), 400

    cursor = conn.cursor()
    cursor.execute('''
    UPDATE workers SET
        worker_id = ?,
        fio = ?,
        position = ?,
        education_level = ?,
        specialty = ?,
        qualification = ?,
        academic_degree = ?,
        academic_title = ?,
        professional_retraining = ?,
        total_experience = ?,
        specialty_experience = ?,
        courses = ?
    WHERE worker_id = ?
    ''', (
        new_worker_id, fio, position, education_level, specialty, qualification,
        academic_degree, academic_title, professional_retraining,
        total_experience, specialty_experience, courses, old_worker_id
    ))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/items')
@login_required
def protected_items():
    return f"Hello, {session['username']}! This is a protected page."
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
@login_required
def protected_assign():
    return f"Hello, {session['username']}! This is a protected page."
def assign():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workers ORDER BY fio ASC')
    workers = cursor.fetchall()

    # Fetch items with their assigned workers
    cursor.execute('''
    SELECT i.item_id, i.name, i.is_specialty, GROUP_CONCAT(w.fio) as workers
    FROM items i
    LEFT JOIN worker_item wi ON i.item_id = wi.item_id
    LEFT JOIN workers w ON wi.worker_id = w.worker_id
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

    # Check if the worker is already assigned to the item
    cursor.execute('SELECT 1 FROM worker_item WHERE worker_id = ? AND item_id = ?', (worker_id, item_id))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('INSERT INTO worker_item (worker_id, item_id) VALUES (?, ?)', (worker_id, item_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    else:
        conn.close()
        return jsonify({'status': 'already_assigned'})

@app.route('/remove_worker_from_item', methods=['POST'])
def remove_worker_from_item():
    data = request.get_json()
    worker_fio = data['worker_fio']
    item_id = data['item_id']

    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    # Fetch worker_id based on FIO
    cursor.execute('SELECT worker_id FROM workers WHERE fio = ?', (worker_fio,))
    worker = cursor.fetchone()

    if worker:
        worker_id = worker[0]
        print(f"Removing worker_id: {worker_id} from item_id: {item_id}")  # Debug print
        cursor.execute('DELETE FROM worker_item WHERE worker_id = ? AND item_id = ?', (worker_id, item_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    else:
        print(f"Worker with FIO: {worker_fio} not found")  # Debug print
        conn.close()
        return jsonify({'status': 'worker_not_found'})

@app.route('/item_workers')
@login_required
def protected_item_workers():
    return f"Hello, {session['username']}! This is a protected page."
def item_workers():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    # Fetch items
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()

    # Fetch worker details for each item
    item_worker_details = {}
    for item in items:
        item_id = item[0]
        cursor.execute('''
        SELECT w.worker_id, w.fio, w.position, w.education_level, w.specialty, w.qualification,
               w.academic_degree, w.academic_title, w.professional_retraining,
               w.total_experience, w.specialty_experience, w.courses
        FROM workers w
        JOIN worker_item wi ON w.worker_id = wi.worker_id
        WHERE wi.item_id = ?
        ''', (item_id,))
        workers = cursor.fetchall()
        item_worker_details[item_id] = workers

    conn.close()
    return render_template('item_workers.html', items=items, item_worker_details=item_worker_details)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True) #server maintain
    app.run(debug=True) #local maintain