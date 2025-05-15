import sqlite3
import random

# Sample data for random selection
last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Васильев"]
first_names = ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей"]
middle_names = ["Иванович", "Петрович", "Алексеевич", "Дмитриевич", "Сергеевич"]
positions = ["Учитель", "Преподаватель", "Профессор", "Доцент", "Ассистент"]
education_levels = ["Среднее", "Бакалавр", "Магистр", "Кандидат наук", "Доктор наук"]
specialties = ["Математика", "Физика", "Химия", "Биология", "Информатика"]
qualifications = ["Высшая", "Первая", "Вторая"]
academic_degrees = ["Кандидат наук", "Доктор наук", None]
academic_titles = ["Доцент", "Профессор", None]
course_options = ["Математический анализ", "Физика твердого тела", "Органическая химия", "Молекулярная биология", "Программирование"]

def setup_database():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workers (
        worker_id INTEGER PRIMARY KEY,
        fio TEXT NOT NULL,
        position TEXT NOT NULL,
        education_level TEXT NOT NULL,
        specialty TEXT NOT NULL,
        qualification TEXT NOT NULL,
        academic_degree TEXT,
        academic_title TEXT,
        professional_retraining TEXT,
        total_experience INTEGER NOT NULL,
        specialty_experience INTEGER NOT NULL,
        courses TEXT NOT NULL
    )
    ''')

    # Insert random data
    for i in range(1, 150):  # Assuming you have 149 workers
        fio = f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(middle_names)}"
        position = random.choice(positions)
        education_level = random.choice(education_levels)
        specialty = random.choice(specialties)
        qualification = random.choice(qualifications)
        academic_degree = random.choice(academic_degrees)
        academic_title = random.choice(academic_titles)
        professional_retraining = "Повышение квалификации" if random.choice([True, False]) else None
        total_experience = random.randint(1, 30)
        specialty_experience = random.randint(1, total_experience)
        courses = ", ".join(random.sample(course_options, random.randint(1, 3)))

        cursor.execute('''
        INSERT INTO workers (
            worker_id, fio, position, education_level, specialty, qualification,
            academic_degree, academic_title, professional_retraining,
            total_experience, specialty_experience, courses
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            i, fio, position, education_level, specialty, qualification,
            academic_degree, academic_title, professional_retraining,
            total_experience, specialty_experience, courses
        ))

    conn.commit()
    conn.close()

# List of specialties and professions
items = [
    ("55.02.02 Анимация", True),
    ("07.02.01 Архитектура", True),
    ("42.02.01 Реклама", True),
    ("54.02.01 Дизайн (по отраслям)", True),
    ("54.02.08 Техника и искусство фотографии", True),
    ("21.02.08/21.02.20 Прикладная геодезия", True),
    ("21.02.04/21.02.19 Землеустройство", True),
    ("21.02.05 Земельно-имущественные отношения 2 г. 10 мес.", True),
    ("21.02.05 Земельно-имущественные отношения 1 г. 10 мес.", True),
    ("21.02.06 Информационные системы обеспечения градостроительной деятельности", True),
    ("15.02.19 Сварочное производство", True),
    ("15.02.19 Сварочное производство (заочное)", True),
    ("08.02.05 Строительство и эксплуатация автомобильных дорог и аэродромов", True),
    ("25.02.08 Эксплуатация беспилотных авиационных систем", True),
    ("08.02.01 Строительство и эксплуатация зданий и сооружений 3г. 10 мес.", True),
     ("08.02.01 Строительство и эксплуатация зданий и сооружений 2г. 10 мес.", True),
    ("08.02.15 Информационное моделирование в строительстве", True),
    ("54.01.20 Графический дизайнер 3г. 10 мес.", False),
    ("54.01.20 Графический дизайнер 1г. 10 мес.", False),
    ("08.01.28 Мастер отделочных строительных и декоративных работ", False),
    ("08.01.27 Мастер общестроительных работ", False),
    ("15.01.05 Сварщик (ручной и частично механизированной сварки (наплавки))", False),
    ("08.01.06 Мастер сухого строительства", False)
]

def update_database():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    # Create new tables for items and worker_item relationships
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        is_specialty BOOLEAN NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS worker_item (
        worker_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (worker_id, item_id),
        FOREIGN KEY (worker_id) REFERENCES workers (worker_id),
        FOREIGN KEY (item_id) REFERENCES items (item_id)
    )
    ''')

    # Insert items if they don't already exist
    for item in items:
        cursor.execute('INSERT OR IGNORE INTO items (name, is_specialty) VALUES (?, ?)', item)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Call the functions to setup and update the database
    setup_database()
    update_database()
