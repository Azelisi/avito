# import asyncio

# from src.parser.database import get_all_ads
# from src.config.check_dub import add_json, read_json, clear_json
# from src.config.cfg import bot
# from src.handlers.basic import sent_notifications, is_running

# # В глобальной области видимости определите структуру данных для хранения уже отправленных уведомлений
# # sent_notifications = {}
# # is_running = False


# async def parse_and_send_notifications(user_id):
#     global is_running
#     is_running = True
#     while is_running:
#         await asyncio.sleep(2)  # 3600 секунд = 1 час
#         # Выполняем парсинг
#         new_ad_text = get_all_ads()

#         # Проверяем, было ли уже отправлено такое уведомление для данного пользователя
#         ad_text = new_ad_text[0][1]  # Предполагаем, что текст объявления находится во втором элементе кортежа
#         formatted_message = format_message(ad_text)  # Форматируем текст объявления
#         if user_id not in sent_notifications:
#             sent_notifications[user_id] = set()

#         if ((formatted_message not in sent_notifications[user_id]) 
#             and not(any(entry.get('content') == formatted_message for entry in read_json(user_id)))):
            
#             # Отправляем уведомление
#             await bot.send_message(user_id, formatted_message, parse_mode="HTML")
#             add_json(user_id, formatted_message)
#             # Добавляем отправленное уведомление в список уже отправленных для данного пользователя
#             sent_notifications[user_id].add(formatted_message)
        
        
#         # Ждем некоторое время перед следующим парсингом
#         print(is_running)
#         await asyncio.sleep(3)


# def format_message(ad_text):
#     # Функция для форматирования текста объявления с использованием HTML-тега <b>
#     format_text = ad_text.split('\n')
#     return "<b>" + "</b>\n<b>".join(format_text) + "</b>"

