# inspect_database.py
import sqlite3

def inspect_database():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()

    # Fetch and print workers
    print("Workers:")
    cursor.execute('SELECT * FROM workers')
    workers = cursor.fetchall()
    for worker in workers:
        print(worker)

    # Fetch and print items
    print("\nItems:")
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    for item in items:
        print(item)

    conn.close()

if __name__ == '__main__':
    inspect_database()
