import sqlite3

conn = sqlite3.connect('ads.db')
cursor = conn.cursor()


# Создание таблицы ads, если она не существует
def create_table_ads():
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS ads (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           text TEXT
       )
   ''')
    conn.commit()


def create_table_subscriptions():
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS subscriptions (
               user_id INTEGER PRIMARY KEY,
               user_subtime INTEGER,
               user_substatus BOOLEAN
           )
      ''')
    conn.commit()


# is_ad_in_database: Проверяет, существует ли объявление (ad_text) в таблице ads.
def is_ad_in_database(ad_text):
    cursor.execute('SELECT * FROM ads WHERE text=?', (ad_text,))
    result = cursor.fetchone()
    return result is not None


# SELECT * FROM ads WHERE text=?: Выполняет запрос на выборку всех записей, где столбец text равен заданному ad_text.
# cursor.fetchone(): Получает одну запись из результата запроса.
# return result is not None: Возвращает True, если запись существует, и False в противном случае.


# save_ad_to_database: Сохраняет объявление (ad_text) в таблицу ads.
def save_ad_to_database(ad_text):
    cursor.execute('SELECT id FROM ads ORDER BY id DESC LIMIT 1')
    last_id = cursor.fetchone()
    if last_id:
        cursor.execute('DELETE FROM ads WHERE id=?', (last_id[0],))
        conn.commit()
        print("Последняя запись удалена")

    cursor.execute('INSERT INTO ads (text) VALUES (?)', (ad_text,))
    conn.commit()


# SELECT id FROM ads ORDER BY id DESC LIMIT 1: Получает id последней записи в таблице.
# cursor.fetchone(): Получает результат запроса.
# DELETE FROM ads WHERE id=?: Удаляет последнюю запись, если она существует.
# INSERT INTO ads (text) VALUES (?): Вставляет новое объявление в таблицу.
# conn.commit(): Сохраняет изменения в базе данных.

# get_all_ads: Получает все записи из таблицы ads.
def get_all_ads():
    cursor.execute('SELECT * FROM ads')
    return cursor.fetchall()

# SELECT * FROM ads: Получает все записи из таблицы.
# cursor.fetchall(): Возвращает список всех записей.
