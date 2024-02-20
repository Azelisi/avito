import sqlite3

from aiogram import F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from datetime import datetime, timedelta
from src.config.cfg import bot
from src.keyboards.inline import return_to_main_kb, menu_kb, MyCallBack
from src.handlers.basic import router

import asyncio

## Обработчик токенов..
@router.callback_query(MyCallBack.filter(F.foo == 'sub' and F.bar == 7))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Отлично!\n', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id=query.message.chat.id,
        title="Подписка",
        description="Подписка на 7 дней",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='7 дней подписки',
                amount=599 * 100
            )
        ],
        max_tip_amount=1000 * 1000,
        suggested_tip_amounts=[],
        start_parameter=f'',
        provider_data=None,
        need_email=False,
        need_phone_number=False,
        need_name=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=True,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=30
    )


@router.callback_query(MyCallBack.filter(F.foo == 'sub' and F.bar == 14))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Отлично!\n', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id= query.message.chat.id,
        title="Подписка",
        description="Подписка на 14 дней",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='14 дней подписки',
                amount=999*100
            )
        ],
        max_tip_amount=1000*1000,
        suggested_tip_amounts=[],
        start_parameter=f'',
        provider_data=None,
        need_email=False,
        need_phone_number=False,
        need_name=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=True,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=30
    ) 


@router.callback_query(MyCallBack.filter(F.foo == 'sub' and F.bar == 30))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Отлично!\n', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id= query.message.chat.id,
        title="Подписка",
        description="Подписка на 14 дней",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='30 дней подписки',
                amount=1799*100
            )
        ],
        max_tip_amount=10000*1000,
        suggested_tip_amounts=[],
        start_parameter=f'',
        provider_data=None,
        need_email=False,
        need_phone_number=False,
        need_name=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=True,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=30
    ) 

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def succesfull_payment(message: Message):
    print("Успешная покупка")
    user_id = message.from_user.id
    price_list = {
        599: 7,
        999: 14,
        1799: 30
    }
    if (message.successful_payment.total_amount//100) in price_list: 
        user_subdays = price_list[message.successful_payment.total_amount//100]
        print(f'{user_subdays} days')
    else: 
        print(f"Ключ {message.successful_payment.total_amount} отсутствует в словаре.")
    user_subtime = 24 * user_subdays # ?? дней подписки (Длительность подписки) 
    user_substatus = True # (Статус подписки (подписан или нет))
     # Рассчитываем время окончания подписки
    expiration_time = int((datetime.now() + timedelta(seconds=user_subtime)).timestamp())
    # Записали user_id в бд и установили время окончания
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Ниже выполняет SQL-запрос для вставки или обновления записи в таблице 'subscriptions'. Используется оператор
    # INSERT OR REPLACE INTO, который вставляет новую запись, если запись с таким user_id не существует, или заменяет
    # существующую запись, если она уже есть. Запрос содержит параметризованные значения (?, ?, ?),
    # которые заменяются значениями переменных user_id, expiration_time и user_substatus. Таким образом, происходит
    # вставка или обновление информации о подписке пользователя в базе данных.
    cursor.execute('''
            INSERT OR REPLACE INTO subscriptions (user_id, expiration_time, is_subscribed)
            VALUES (?, ?, ?)
        ''', (user_id, expiration_time, user_substatus))
    conn.commit()
    conn.close()

    msg = f"Спасибо за покупку {message.successful_payment.total_amount // 100} {message.successful_payment.currency}!"
    await message.answer(f"{msg}\nПожалуйста, выбери, что ты хочешь сделать", reply_markup=menu_kb)