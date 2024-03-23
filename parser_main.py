import asyncio
import sqlite3
import time

from bs4 import BeautifulSoup
from selenium import webdriver
import pyshorteners
from src.config.cfg import url_Avito
from src.parser.database import create_table_ads, is_ad_in_database, save_ad_to_database

from src.config.cfg import url_Avito
from src.parser.database import create_table_ads, is_ad_in_database, save_ad_to_database

# Создаем подключение к базе данных
conn = sqlite3.connect('ads.db')
cursor = conn.cursor()

create_table_ads()

url = url_Avito
options = webdriver.ChromeOptions()
options.add_argument("--headless")


def shorten_url(long_url):
    short_link = pyshorteners.Shortener()
    return short_link.tinyurl.short(long_url)


def pars():
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
        # street = bs.find("div", class_="geo-root-zPwRk")
        link_product_source = bs.find("div", class_="iva-item-title-py3i_")
        link_product = link_product_source.find("a", class_="styles-module-root-QmppR")
        print("Парсер работет")

        # Закрытие веб-драйвера
        driver.quit()

        # Проход по каждому блоку с информацией о заявке
        for ad_block in ad_blocks:
            shortened_img_url = shorten_url(img['src'])
            # Формируем текст объявления
            ad_text = (
                f"Ссылка:\n"
                f"https://www.avito.ru{link_product['href']}\n"
                f"Название: {title.text}\n"
                f"Цена: {price.text}\n"
                f"Описание: {description.text}\n\n"
                # f"Район: {street.text}\n"
                f"Картинка: {shortened_img_url}"
            )

            # Проверяем, есть ли объявление уже в базе данных
            if not is_ad_in_database(ad_text):
                # Отправляем уведомление в Telegram
                print(f"Новая запись: {title.text}\nЦена: {price.text}")
                save_ad_to_database(ad_text)

                print("Запись в базу")
                # Здесь скрипт возвращает ad_text
                print("ad_text вернулся")
                return ad_text
            else:
                print("Вернулся 0")
                return 0

    except Exception as errorException:
        print(f"Произошла ошибка: {errorException}")
        print("Перезапуск программы через 5 секунд...")
        asyncio.sleep(5)  # Подождем перед следующей попыткой


conn.close()


def run_parser():
    while True:
        pars()
        time.sleep(10)


run_parser()
