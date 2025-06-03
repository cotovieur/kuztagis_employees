#app.py
import sqlite3
import shutil
import os
from datetime import datetime, timedelta
import atexit
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import threading
import time
import json
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

# Global variable to track the number of changes
change_count = 0
last_backup_time = datetime.now()

# Log file path
LOG_FILE = 'changes.log'

def log_action(username, action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - User: {username} - Action: {action} - Details: {details}\n"

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)

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
                log_action(username, 'login', 'User logged in')
                flash('Успешный вход!')
                return redirect(url_for('index'))

        flash('Неверный логин/пароль!')
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
    if username:
        log_action(username, 'logout', 'User logged out')
    flash('Успешный выход!')
    return redirect(url_for('login'))

@app.route('/workers')
@login_required
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
def add_worker():
    if request.method == 'POST':
        username = session.get('username')
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
        log_action(username, 'add_worker', f'Added worker: {fio}')

        # Increment change count
        increment_change_count()

        # Check if backup is needed based on changes
        if should_backup_based_on_changes():
            backup_database('workers.db', 'backups')

        conn.close()
        return jsonify({'status': 'success'})

    return render_template('add_worker.html')

# Firing worker
@app.route('/fire', methods=['POST'])
def fire_worker():
    username = session.get('username')
    data = request.get_json()
    worker_id = data['worker_id']

    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    # Fetch worker details for logging
    cursor.execute('SELECT fio FROM workers WHERE worker_id = ?', (worker_id,))
    worker = cursor.fetchone()

    fio = worker[0]
    print(f"Firing worker_id: {worker_id}")  # Debug print
    cursor.execute('DELETE FROM workers WHERE worker_id = ?', (worker_id,))

    # Delete the worker from the worker_item table
    cursor.execute('DELETE FROM worker_item WHERE worker_id = ?', (worker_id,))

    conn.commit()
    log_action(username, 'fire_worker', f'Fired worker: {fio}')

    # Increment change count
    increment_change_count()

    # Check if backup is needed based on changes
    if should_backup_based_on_changes():
        backup_database('workers.db', 'backups')

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
    username = session.get('username')
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

    # Fetch current worker details for comparison
    cursor.execute('SELECT * FROM workers WHERE worker_id = ?', (old_worker_id,))
    current_worker = cursor.fetchone()

    if current_worker:
        # Prepare a list to store changes
        changes = []

        # Compare each field and log changes
        fields = [
            ('worker_id', new_worker_id),
            ('fio', fio),
            ('position', position),
            ('education_level', education_level),
            ('specialty', specialty),
            ('qualification', qualification),
            ('academic_degree', academic_degree),
            ('academic_title', academic_title),
            ('professional_retraining', professional_retraining),
            ('total_experience', total_experience),
            ('specialty_experience', specialty_experience),
            ('courses', courses)
        ]

        # Field indices in the current_worker tuple
        field_indices = {
            'worker_id': 0,
            'fio': 1,
            'position': 2,
            'education_level': 3,
            'specialty': 4,
            'qualification': 5,
            'academic_degree': 6,
            'academic_title': 7,
            'professional_retraining': 8,
            'total_experience': 9,
            'specialty_experience': 10,
            'courses': 11
        }

        # Check each field for changes
        for field_name, new_value in fields:
            old_value = current_worker[field_indices[field_name]]
            if old_value != new_value:
                changes.append(f"{field_name}: '{old_value}' changed to '{new_value}'")

        # Log changes if any
        if changes:
            log_action(username, 'edit_worker', f"Edited worker: {fio}. Changes: {', '.join(changes)}")
        else:
            log_action(username, 'edit_worker', f"No changes detected for worker: {fio}")

    # Update worker details
    
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

    # Increment change count
    increment_change_count()

    # Check if backup is needed based on changes
    if should_backup_based_on_changes():
        backup_database('workers.db', 'backups')
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/items')
@login_required
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

        # Increment change count
        increment_change_count()

        # Check if backup is needed based on changes
        if should_backup_based_on_changes():
            backup_database('workers.db', 'backups')

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

        # Increment change count
        increment_change_count()

        # Check if backup is needed based on changes
        if should_backup_based_on_changes():
            backup_database('workers.db', 'backups')

        conn.close()
        return jsonify({'status': 'success'})
    else:
        print(f"Worker with FIO: {worker_fio} not found")  # Debug print
        conn.close()
        return jsonify({'status': 'worker_not_found'})

@app.route('/item_workers')
@login_required
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

def backup_database(db_path, backup_dir):
    global change_count, last_backup_time
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")

    shutil.copy2(db_path, backup_path)
    print(f"Database backed up to {backup_path}")

    # Reset change count and update last backup time
    change_count = 0
    last_backup_time = datetime.now()

def perform_backup_on_exit(db_path, backup_dir):
    print("Performing backup before exiting...")
    backup_database(db_path, backup_dir)

def should_backup_based_on_changes():
    global change_count, last_backup_time
    # Check if the number of changes exceeds the threshold
    if change_count >= 20:
        return True

    # Check if a week has passed since the last backup
    if (datetime.now() - last_backup_time) >= timedelta(days=7):
        return True

    return False

def increment_change_count():
    global change_count
    change_count += 1


if __name__ == '__main__':
    db_path = 'workers.db'
    backup_dir = 'backups'

    # Register the backup function to be called on exit
    atexit.register(perform_backup_on_exit, db_path, backup_dir)

    #app.run(host='0.0.0.0', port=5000, debug=True) #server maintain
    app.run(debug=True) #local maintain