from src.config.cfg import bot, dp
from src.handlers import basic, payments
from src.parser.parser import pars
import logging
import asyncio


async def on_startup(dispatcher):
    print("Бот запущен")


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    dp.include_routers(basic.router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
    pars()
