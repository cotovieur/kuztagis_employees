# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workers')
    workers = cursor.fetchall()
    conn.close()
    return render_template('index.html', workers=workers)

@app.route('/add', methods=['GET', 'POST'])
def add_worker():
    if request.method == 'POST':
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
            fio, position, education_level, specialty, qualification,
            academic_degree, academic_title, professional_retraining,
            total_experience, specialty_experience, courses
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fio, position, education_level, specialty, qualification,
            academic_degree, academic_title, professional_retraining,
            total_experience, specialty_experience, courses
        ))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_worker.html')

if __name__ == '__main__':
    app.run(debug=True)
