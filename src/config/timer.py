import asyncio
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def timer_db():
    print("Фу")
    while True:
        # await asyncio.sleep(60 * 60 * 12)  # Обновление каждые 12 часов
        await asyncio.sleep(10)
        print("10 sec")
        # Подключение к базе данных
        conn_sub = sqlite3.connect('subscriptions.db')
        cursor = conn_sub.cursor()
        # Получаем одну запись из таблицы subscriptions
        cursor.execute('SELECT user_id, user_subtime, user_substatus FROM subscriptions')
        subscription = cursor.fetchone()

        while subscription:
            user_id, expiration_time, is_subscribed = subscription
            # Уменьшаем время подписки на 12 часов
            expiration_time -= 12
            print('СЧИТАЕМ')
            # Если время подписки меньше или равно 0, устанавливаем статус подписки в False
            if expiration_time <= 0:
                expiration_time = 0
                is_subscribed = False

            # Обновляем запись в базе данных
            cursor.execute('''
                UPDATE subscriptions
                SET user_subtime=?, user_substatus=?
                WHERE user_id=?
            ''', (expiration_time, is_subscribed, user_id))

            # Получаем следующую запись
            subscription = cursor.fetchone()

        # Сохраняем изменения и закрываем подключение к базе данных
        conn_sub.commit()
        conn_sub.close()
