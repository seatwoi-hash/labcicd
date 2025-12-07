import sqlite3

def init_db(name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()


def get_db_connection(name_db):
    conn = sqlite3.connect(name_db)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(name_db, name, email):
    conn = get_db_connection(name_db)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        (name, email)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_users(name_db):
    conn = get_db_connection(name_db)
    cursor = conn.cursor()
    list_users = cursor.execute(
        'SELECT * FROM users'
    )
    return list_users
