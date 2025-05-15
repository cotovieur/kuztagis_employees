# # setup_database.py
# import sqlite3
# import random

# # Sample data for random selection
# last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Васильев"]
# first_names = ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей"]
# middle_names = ["Иванович", "Петрович", "Алексеевич", "Дмитриевич", "Сергеевич"]
# positions = ["Учитель", "Преподаватель", "Профессор", "Доцент", "Ассистент"]
# education_levels = ["Среднее", "Бакалавр", "Магистр", "Кандидат наук", "Доктор наук"]
# specialties = ["Математика", "Физика", "Химия", "Биология", "Информатика"]
# qualifications = ["Высшая", "Первая", "Вторая"]
# academic_degrees = ["Кандидат наук", "Доктор наук", None]
# academic_titles = ["Доцент", "Профессор", None]
# course_options = ["Математический анализ", "Физика твердого тела", "Органическая химия", "Молекулярная биология", "Программирование"]

# def setup_database():
#     conn = sqlite3.connect('workers.db')
#     cursor = conn.cursor()

#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS workers (
#         worker_id INTEGER PRIMARY KEY,
#         fio TEXT NOT NULL,
#         position TEXT NOT NULL,
#         education_level TEXT NOT NULL,
#         specialty TEXT NOT NULL,
#         qualification TEXT NOT NULL,
#         academic_degree TEXT,
#         academic_title TEXT,
#         professional_retraining TEXT,
#         total_experience INTEGER NOT NULL,
#         specialty_experience INTEGER NOT NULL,
#         courses TEXT NOT NULL
#     )
#     ''')

#     # Insert random data
#     for i in range(1, 150):  # Assuming you have 149 workers
#         fio = f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(middle_names)}"
#         position = random.choice(positions)
#         education_level = random.choice(education_levels)
#         specialty = random.choice(specialties)
#         qualification = random.choice(qualifications)
#         academic_degree = random.choice(academic_degrees)
#         academic_title = random.choice(academic_titles)
#         professional_retraining = "Повышение квалификации" if random.choice([True, False]) else None
#         total_experience = random.randint(1, 30)
#         specialty_experience = random.randint(1, total_experience)
#         courses = ", ".join(random.sample(course_options, random.randint(1, 3)))

#         cursor.execute('''
#         INSERT INTO workers (
#             worker_id, fio, position, education_level, specialty, qualification,
#             academic_degree, academic_title, professional_retraining,
#             total_experience, specialty_experience, courses
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             i, fio, position, education_level, specialty, qualification,
#             academic_degree, academic_title, professional_retraining,
#             total_experience, specialty_experience, courses
#         ))

#     conn.commit()
#     conn.close()

# if __name__ == '__main__':
#     setup_database()
