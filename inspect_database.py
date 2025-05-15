# inspect_database.py
import sqlite3

def inspect_database():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM workers')
    workers = cursor.fetchall()

    for worker in workers:
        print(worker)

    conn.close()

if __name__ == '__main__':
    inspect_database()