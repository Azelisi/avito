import asyncio
import sqlite3

from datetime import datetime, timedelta

from aiogram import F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from src.config.cfg import bot
from src.keyboards.inline import return_to_main_kb, menu_kb, MyCallBack
from src.handlers.basic import router


conn = sqlite3.connect('subscriptions.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER PRIMARY KEY,
    end_time TIMESTAMP
)
''')
conn.commit()


async def send_subscription_expired_message(user_id: int):
    await bot.send_message(user_id, "Ваша подписка истекла. Пожалуйста, продлите её.")

# Функция для отслеживания времени подписки
async def subscription_timer(user_id: int, end_time: datetime):
    while datetime.now() < end_time:
        await asyncio.sleep(60 * 60 * 24)  # Проверяем каждый день
    await send_subscription_expired_message(user_id)

# Обработчик команды для начала подписки
@router.message(commands=['subscribe'])
async def subscribe(message: Message):
    user_id = message.from_user.id
    duration = 7  # Например, подписка на неделю
    
    # Рассчитываем время окончания подписки
    end_time = datetime.now() + timedelta(days=duration)
    
    # Записываем информацию в базу данных
    cursor.execute('''
    INSERT OR REPLACE INTO subscriptions (user_id, end_time) VALUES (?, ?)
    ''', (user_id, end_time))
    conn.commit()
    
    # Запускаем таймер подписки
    asyncio.create_task(subscription_timer(user_id, end_time))
    
    await message.reply("Вы успешно подписаны!")

# Проверяем подписки при запуске бота
async def check_subscriptions():
    cursor.execute('SELECT user_id, end_time FROM subscriptions')
    for row in cursor.fetchall():
        user_id, end_time = row
        if datetime.now() < end_time:
            asyncio.create_task(subscription_timer(user_id, end_time))
        else:
            await send_subscription_expired_message(user_id)

