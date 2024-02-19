import sqlite3
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from src.config.cfg import url_Avito

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

url = url_Avito
options = webdriver.ChromeOptions()
options.add_argument("--headless")

def pars(): 
    while True:
        try:
            driver = webdriver.Chrome(options=options)
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
            link_product_source = bs.find("div", class_="iva-item-title-py3i_")
            link_product = link_product_source.find("a", class_="styles-module-root-QmppR")
            print("Парсер работет")

            # Закрытие веб-драйвера
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
                    print(f"Новая запись: {title.text}\nЦена: {price.text}")
                    save_ad_to_database(ad_text)
                    print("Запись в базу")
                    time.sleep(40)

        except Exception as errorException:
            print(f"Произошла ошибка: {errorException}")
            print("Перезапуск программы через 30 секунд...")
            time.sleep(30)  # Подождем перед следующей попыткой

pars()

print(1231231)