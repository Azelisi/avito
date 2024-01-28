import sqlite3
import asyncio
from time import sleep

from aiogram.filters import Command
from config import telegram_token, url_Avito
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from selenium import webdriver

bot = Bot(token=telegram_token)
dp = Dispatcher()

options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Создаем подключение к базе данных
conn = sqlite3.connect('ads.db')
cursor = conn.cursor()

# Создаем таблицу, если её нет
cursor.execute('''
       CREATE TABLE IF NOT EXISTS ads (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           text TEXT
       )
   ''')
conn.commit()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для уведомлений об объявлениях Авито. \n\nСейчас я начну отправлять объявления")
    print("User start")

    while True:
        try:
            await check_ads(message.chat.id)
        except Exception as errorException:
            print(f"Произошла ошибка: {errorException}")
            print("Перезапуск программы через 30 секунд...")
            sleep(30)  # Подождем минуту перед следующей попыткой


async def check_ads(chat_id):
    url = url_Avito
    # Инициализация веб-драйвера
    driver = webdriver.Chrome(options=options)
    try:

        driver.get(url)
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        # Найти все блоки с информацией о заявках
        ad_blocks = bs.find_all("div", class_="iva-item-content-rejJg")

        # Проход по каждому блоку с информацией о заявке
        # for ad_block in ad_blocks
        # Здесь вы можете извлекать нужную информацию из блока
        # Например, название и цену
        img = bs.find("img", class_="photo-slider-image-YqMGj")
        title = bs.find("h3", class_="styles-module-size_l_compensated-OK6a6")
        price = bs.find("div", class_="iva-item-priceStep-uq2CQ")
        description = bs.find("div", class_="iva-item-descriptionStep-C0ty1")
        street = bs.find("div", class_="geo-root-zPwRk")
        # time = bs.find("div", class_="iva-item-dateInfoStep-_acjp") Пока не работает
        link_product_source = bs.find("div", class_="iva-item-title-py3i_")
        link_product = link_product_source.find("a", class_="styles-module-root-QmppR")
        print("Парсер работет")
    finally:
        # Закрытие веб-драйвера в блоке finally, чтобы гарантировать его закрытие
        driver.quit()

    def is_ad_in_database(ad_text):
        # Проверяем, есть ли объявление в базе данных
        cursor.execute('SELECT * FROM ads WHERE text=?', (ad_text,))
        result = cursor.fetchone()

        return result is not None

    def save_ad_to_database(ad_text):
        # Удаляем последнюю запись
        cursor.execute('SELECT id FROM ads ORDER BY id DESC LIMIT 1')
        last_id = cursor.fetchone()
        if last_id:
            cursor.execute('DELETE FROM ads WHERE id=?', (last_id[0],))
            conn.commit()
            print("Последняя запись удалена")

        # Сохраняем объявление в базе данных
        cursor.execute('INSERT INTO ads (text) VALUES (?)', (ad_text,))
        conn.commit()

    # Проход по каждому блоку с информацией о заявке
    for ad_block in ad_blocks:

        # Формируем текст объявления
        ad_text = (
            f"\n{img['src']}\n"
            f"Название: {title.text}\n"
            f"Цена: {price.text}\n"
            f"Описание: {description.text}\n"
            f"Район: {street.text}\n"
            f"Ссылка: "
            f"https://www.avito.ru{link_product['href']}"
        )

        # Проверяем, есть ли объявление уже в базе данных
        if not is_ad_in_database(ad_text):
            # Отправляем уведомление в Telegram
            print(f"Новая запись: {ad_text}")
            save_ad_to_database(ad_text)
            await bot.send_message(chat_id, f"Новая запись: {ad_text}")
            print("Запись в базу")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Произошла ошибка при запуске программы: {e}")
        print("Перезапуск программы через 60 секунд...")
        sleep(60)  # Подождем минуту перед следующей попыткой
