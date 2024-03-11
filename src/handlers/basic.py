import sqlite3

from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.cfg import bot
from src.parser.parser import pars
from src.keyboards.inline import menu_kb, return_to_main_kb, payment_kb, how_many_day_sub_banks, how_many_day_sub_crypt, MyCallBack, type_of_payment
from src.handlers.cryptomus import create_invoice, get_invoice
from src.parser.database import get_all_ads


import random

import asyncio

# from src.rabbitmq.rabbitmq import RabbitMQSender

# rabbitmq_sender = RabbitMQSender()

router = Router()


# result_pars = pars()

# Роутер основного меню..

@router.message(F.text == '/start')
async def get_talk(message: Message, state: FSMContext):
    await message.reply("Привет, я бот-парсер!", reply_markup=menu_kb)


# Роутер возвращения...

@router.callback_query(MyCallBack.filter(F.foo == 'return_to_main'))
async def get_to_main(query: CallbackQuery, callback_data: MyCallBack):
    await query.answer("Основное меню")
    await query.message.edit_text("Пожалуйста, выбери, что ты хочешь сделать", reply_markup=menu_kb)

@router.callback_query(MyCallBack.filter(F.foo == 'return_typeOfPay'))
async def get_to_main(query: CallbackQuery, callback_data: MyCallBack):
    await query.message.edit_text("Выбери способ оплаты", reply_markup=type_of_payment)

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
        "Выбери способ оплаты", reply_markup=type_of_payment)

# Для банков
@router.callback_query(MyCallBack.filter(F.foo == 'pay_bank'))
async def top_up_user_bank(query: CallbackQuery, callback_data: MyCallBack):
    await query.message.edit_text(
        "Оформить подписку\n\n7 дней - <b>599 RUB</b>\n14 дней - <b>999 RUB</b>\n30 дней - <b>1799 RUB</b>",
        parse_mode='HTML', reply_markup=how_many_day_sub_banks)

# Для крипты 
@router.callback_query(MyCallBack.filter(F.foo == 'pay_crypt'))
async def top_up_user_crypt(query: CallbackQuery, callback_data: MyCallBack):
    await query.message.edit_text(
        "Оформить подписку\n\n7 дней - <b>599 RUB</b>\n14 дней - <b>999 RUB</b>\n30 дней - <b>1799 RUB</b>",
        parse_mode='HTML', reply_markup=how_many_day_sub_crypt)

@router.callback_query(MyCallBack.filter(F.foo == 'sub_crypt_7'))
async def top_up_user_crypt_7(query: CallbackQuery, callback_data: MyCallBack):
    invoice = await create_invoice(query.message.from_user.id, 599)
    markup = InlineKeyboardBuilder().button(text="✅ Я оплатил", callback_data=f'o_{invoice["result"]["uuid"]}')
    await query.message.edit_text(f"Ваш чек: {invoice['result']['url']} ", reply_markup=markup)

@router.callback_query(MyCallBack.filter(F.foo == 'sub_crypt_14'))
async def top_up_user_crypt_14(query: CallbackQuery, callback_data: MyCallBack):
    invoice = await create_invoice(query.message.from_user.id, 999)
    markup = InlineKeyboardBuilder().button(text="✅ Я оплатил", callback_data=f'o_{invoice["result"]["uuid"]}')
    await query.message.edit_text(f"Ваш чек: {invoice['result']['url']} ", reply_markup=markup)


@router.callback_query(MyCallBack.filter(F.foo == 'sub_crypt_30'))
async def top_up_user_crypt_30(query: CallbackQuery, callback_data: MyCallBack):
    invoice = await create_invoice(query.message.from_user.id, 1799)
    markup = InlineKeyboardBuilder().button(text="✅ Я оплатил", callback_data=f'o_{invoice["result"]["uuid"]}')
    await query.message.edit_text(f"Ваш чек: {invoice['result']['url']} ", reply_markup=markup)

    
# Роутер парсинга..
# Проверка в базе на то что пользователь подписан (то есть, смотрим в базу данных user_id и sub_status и если sub_status равен 1 то всё заебисб)
@router.callback_query(MyCallBack.filter(F.foo == 'parsing'))
async def start_process_of_pars(query: types.CallbackQuery, callback_data: MyCallBack):
    user_id = query.from_user.id
    print(f"Start parsing cycle for user {user_id}")
    conn_sub = sqlite3.connect('subscriptions.db')
