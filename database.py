import sqlite3

def create_user_table():
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        query = '''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        tg_username TEXT UNIQUE,
        real_name TEXT,
        age INTEGER,
        number INTEGER
        )
        '''
        cur.execute(query)
        con.commit()


def insert_into_user_table(
        tg_username,
        real_name,
        age,
        number
    ):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        query = 'INSERT INTO users(tg_username, real_name, age, number) VALUES(?, ?, ?, ?)'
        cur.execute(query, (tg_username, real_name, age, number))
        con.commit()


def get_all_users():
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        query = '''
        SELECT tg_username, real_name, age, number FROM users
        ORDER BY id
        '''
        cur.execute(query)
        return cur.fetchall()


def get_my_info(tg_username):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        query = '''
        SELECT tg_username, real_name, age, number FROM users
            WHERE tg_username = ?
        '''
        cur.execute(query, (tg_username,))
        return cur.fetchone()


def drop_table():
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        query = 'DROP TABLE users'
        cur.execute(query)


create_user_table()