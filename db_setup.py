import sqlite3
import csv
import re

# Function to convert experience string to years
def convert_experience_to_years(experience_str):
    if not experience_str:
        return 0
    # Extract numbers from the string
    numbers = re.findall(r'\d+', experience_str)
    if not numbers:
        return 0
    # Convert the first number to integer
    return int(numbers[0])

# Connect to the existing SQLite database
conn = sqlite3.connect('workers.db')
cursor = conn.cursor()

# Open the CSV file and read the data with a different encoding
with open('C:\\Users\\Клинцов\\Downloads\\Personal&allpages=1 (2).csv', mode='r', encoding='cp1251') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        # Extract and convert data
        worker_id = int(row[1])  # Second column
        fio = row[2]  # Third column
        experience_str = row[-1]  # Last column
        total_experience = convert_experience_to_years(experience_str)

        # Insert data into the database
        cursor.execute('''
        INSERT OR REPLACE INTO workers (worker_id, fio, position, education_level, specialty, qualification, academic_degree, academic_title, professional_retraining, total_experience, specialty_experience, courses)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (worker_id, fio, 'position', 'education_level', 'specialty', 'qualification', 'academic_degree', 'academic_title', 'professional_retraining', total_experience, total_experience, 'courses'))

# Commit the changes and close the connection
conn.commit()
conn.close()
