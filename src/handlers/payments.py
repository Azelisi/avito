from aiogram import F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from src.config.cfg import bot
from src.keyboards.inline import return_to_main_kb, MyCallBack
from src.handlers.basic import router

import asyncio

## Обработчик токенов..
@router.callback_query(MyCallBack.filter(F.foo == 'tokens' and F.bar == 1))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Неплохой выбор\nПосле оплаты нажми кнопку "Назад"', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id= query.message.chat.id,
        title="Покупка токенов",
        description="Купить 1 токен",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='1 токен',
                amount=399*100
            )
        ],
        max_tip_amount=1000*1000,
        suggested_tip_amounts=[100*100,300*100],
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


## 
@router.callback_query(MyCallBack.filter(F.foo == 'tokens' and F.bar == 5))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Хороший выбор\nПосле оплаты нажми кнопку "Назад"', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id= query.message.chat.id,
        title="Покупка токенов",
        description="Купить 5 токенов",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='5 токенов',
                amount=799*100
            )
        ],
        max_tip_amount=1000*1000,
        suggested_tip_amounts=[100*100,300*100],
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

## 
@router.callback_query(MyCallBack.filter(F.foo == 'tokens' and F.bar == 10))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Лучший выбор\nПосле оплаты нажми кнопку "Назад"', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id= query.message.chat.id,
        title="Покупка токенов",
        description="Купить 10 токенов",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='10 токенов',
                amount=1399*100
            )
        ],
        max_tip_amount=1000*1000,
        suggested_tip_amounts=[100*100,300*100],
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

