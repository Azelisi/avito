import sqlite3

from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from src.config.cfg import bot
from src.keyboards.inline import menu_kb, return_to_main_kb, payment_kb, how_many_day_sub, MyCallBack
from src.parser.parser import pars
from src.parser.database import get_all_ads
from src.config.states import ParserStates



import random
import asyncio

router = Router()
# result_pars = pars()

# Роутер основного меню..

@router.message(F.text == '/start')
async def get_talk(message: Message, state: FSMContext):
    await message.reply("Привет, я бот-парсер!", reply_markup=menu_kb)


# Роутер возвращения в основное меню..

@router.callback_query(MyCallBack.filter(F.foo == 'return_to_main'))
async def get_to_main(query: CallbackQuery, callback_data: MyCallBack, state: FSMContext):
    await state.set_state(ParserStates.main_menu)
    await query.answer("Основное меню")
    await query.message.edit_text("Пожалуйста, выбери, что ты хочешь сделать", reply_markup=menu_kb)


# Роутер информации для пользователя..

@router.callback_query(MyCallBack.filter(F.foo == 'info'))
async def callback_info(query: CallbackQuery, callback_data: MyCallBack):
    await query.answer("Информация о парсинге")
    await query.message.edit_text('Важно знать перед использованием!\nВот как выполняется парсинг',
                                  reply_markup=return_to_main_kb)


# Роутер для пополнения счёта пользователя..

@router.callback_query(MyCallBack.filter(F.foo == 'pay'))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack):
    await query.message.edit_text(
        "Оформить подписку\n\n7 дней - <b>599 RUB</b>\n14 дней - <b>999 RUB</b>\n30 дней - <b>1799 RUB</b>",
        parse_mode='HTML', reply_markup=how_many_day_sub)


# Роутер парсинга..
# Проверка в базе на то что пользователь подписан (то есть, смотрим в базу данных user_id и sub_status и если sub_status равен 1 то всё заебисб)
@router.callback_query(MyCallBack.filter(F.foo == 'parsing'))
async def start_process_of_pars(query: CallbackQuery, callback_data: MyCallBack, state: FSMContext):
    user_id = query.from_user.id
    conn_sub = sqlite3.connect('subscriptions.db')
    cursor = conn_sub.cursor()

    cursor.execute('SELECT user_substatus FROM subscriptions WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        await state.set_state(ParserStates.parsing)
        new_ad_text = get_all_ads()
        old_ad_text = None

        while True:
            if new_ad_text != [] and (old_ad_text is None or old_ad_text[0] != new_ad_text[0]):  # Проверка состояния бота, которое указал пользователь
                old_ad_text = new_ad_text 
                await query.message.answer(f"{new_ad_text[0]}", reply_markup=return_to_main_kb)
            else:
                await asyncio.sleep(1)  # Добавим небольшую задержку, чтобы не нагружать процессор
            # Проверяем, была ли нажата кнопка "Назад"
            if await state.get_state() == 'main_menu':
                break  # Если кнопка нажата, выходим из цикла
    else:
        await query.message.edit_text("Извини, но на твоём балансе недостаточно средств для выполнения процедуры парса",
                                      reply_markup=payment_kb)

