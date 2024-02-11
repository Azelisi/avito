from aiocron import crontab

from avito.src.config.cfg import bot
from avito.src.parser.database import get_all_ads


# Задача будет выполняться каждую минуту
### crontab засунь в manager.py
@crontab('* */1 * * *')
async def send_notifications(user_id):
    ads = get_all_ads()
    for ad in ads:
        ### user_id = 123456789  Замени на  пользователя, которому нужно отправить уведомление(или масив)
        await bot.send_message(user_id, ad[1])  # Предполагается, что текст объявления находится во втором столбце
