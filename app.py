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

# Adding new worker
@app.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
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

if __name__ == '__main__':
    app.run(debug=True)
