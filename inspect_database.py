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

    # Fetch and print worker-item relationships with names and titles
    print("\nWorker-Item Relationships:")
    cursor.execute('''
    SELECT w.fio, i.name
    FROM worker_item wi
    JOIN workers w ON wi.worker_id = w.worker_id
    JOIN items i ON wi.item_id = i.item_id
    ''')
    worker_items = cursor.fetchall()
    for worker_item in worker_items:
        print(worker_item)

    conn.close()

if __name__ == '__main__':
    inspect_database()
