import sqlite3

from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from src.config.cfg import bot
from src.keyboards.inline import menu_kb, return_to_main_kb, payment_kb, how_many_day_sub, MyCallBack
from src.parser.database import get_all_ads

import asyncio

from src.rabbitmq.rabbitmq import RabbitMQSender

rabbitmq_sender = RabbitMQSender()

router = Router()


# result_pars = pars()

# Роутер основного меню..

@router.message(F.text == '/start')
async def get_talk(message: Message, state: FSMContext):
    await message.reply("Привет, я бот-парсер!", reply_markup=menu_kb)


# Роутер возвращения в основное меню..

@router.callback_query(MyCallBack.filter(F.foo == 'return_to_main'))
async def get_to_main(query: CallbackQuery, callback_data: MyCallBack):
    await query.answer("Основное меню")
    await query.message.edit_text("Пожалуйста, выбери, что ты хочешь сделать", reply_markup=menu_kb)
    print(f'{query.data} and {type(query.data)}')


# Роутер информации для пользователя..

@router.callback_query(MyCallBack.filter(F.foo == 'info'))
async def callback_info(query: CallbackQuery, callback_data: MyCallBack):
    await query.answer("Информация о парсинге")
    await query.message.edit_text('Важно знать перед использованием!\nВот как выполняется парсинг',
                                  reply_markup=return_to_main_kb)
    print(f'{query.data} and {type(query.data)}')


# Роутер для пополнения счёта пользователя..

@router.callback_query(MyCallBack.filter(F.foo == 'pay'))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack):
    await query.message.edit_text(
        "Оформить подписку\n\n7 дней - <b>599 RUB</b>\n14 дней - <b>999 RUB</b>\n30 дней - <b>1799 RUB</b>",
        parse_mode='HTML', reply_markup=how_many_day_sub)


# Роутер парсинга..
# Проверка в базе на то что пользователь подписан (то есть, смотрим в базу данных user_id и sub_status и если sub_status равен 1 то всё заебисб)
@router.callback_query(MyCallBack.filter(F.foo == 'parsing'))
async def start_process_of_pars(query: types.CallbackQuery, callback_data: MyCallBack):
    user_id = query.from_user.id
    print(f"Start parsing cycle for user {user_id}")
    conn_sub = sqlite3.connect('subscriptions.db')
    cursor = conn_sub.cursor()

    cursor.execute('SELECT user_substatus FROM subscriptions WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        new_ad_text = get_all_ads()
        old_ad_text = None

        while True:
            input_string = query.data
            parts = input_string.split(":")
            middle_word = parts[1]
            print(middle_word)
            if middle_word == 'return_to_main':
                break
            else:
                old_ad_text = new_ad_text

                # Отправляем сообщение в очередь RabbitMQ с ключом, равным идентификатору пользователя
                print(f"Sending message to RabbitMQ for user {user_id}")
                rabbitmq_sender.send_message(f'user_{user_id}', {'text': f'{new_ad_text[0]}'})
                await asyncio.sleep(15)
    else:
        await query.message.edit_text("Извини, но на твоём балансе недостаточно средств для выполнения процедуры парса",
                                      reply_markup=how_many_day_sub)
# @router.callback_query(SwitchStatesGroup.main)
# async def callback_handler(query: types.CallbackQuery, state: FSMContext):
#     await state.set_state(ParsingAvito.main)
