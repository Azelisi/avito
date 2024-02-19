import sqlite3

conn = sqlite3.connect('ads.db')
cursor = conn.cursor()


def create_table():
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS ads (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           text TEXT
       )
   ''')
    conn.commit()


def is_ad_in_database(ad_text):
    cursor.execute('SELECT * FROM ads WHERE text=?', (ad_text,))
    result = cursor.fetchone()
    return result is not None


def save_ad_to_database(ad_text):
    cursor.execute('SELECT id FROM ads ORDER BY id DESC LIMIT 1')
    last_id = cursor.fetchone()
    if last_id:
        cursor.execute('DELETE FROM ads WHERE id=?', (last_id[0],))
        conn.commit()
        print("Последняя запись удалена")

    cursor.execute('INSERT INTO ads (text) VALUES (?)', (ad_text,))
    conn.commit()


def get_all_ads():
    cursor.execute('SELECT * FROM ads')
    return cursor.fetchall()


