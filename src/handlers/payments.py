from aiogram import F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from src.config.cfg import bot
from src.keyboards.inline import return_to_main_kb, menu_kb, MyCallBack
from src.handlers.basic import router

import asyncio

## Обработчик токенов..
@router.callback_query(MyCallBack.filter(F.foo == 'tokens' and F.bar == 1))
async def top_up_user(query: CallbackQuery, callback_data: MyCallBack): 
    await query.message.edit_text('Неплохой выбор\nПосле оплаты нажми кнопку "Назад"', reply_markup=return_to_main_kb)
    await bot.send_invoice(
        chat_id= query.message.chat.id,
        title="Подписка",
        description="Подписка на 1 месяц",
        payload=f'test-invoice-payload',
        provider_token='381764678:TEST:68132',
        currency='RUB',
        prices=[
            LabeledPrice(
                label='Месяц подписки',
                amount=599*100
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

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):

    if pre_checkout_query.invoice_payload != "test_payload":
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="errors gere...")
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def succesfull_payment(message: Message):
    print("Успешная покупка")
    msg = f"Спасибо за покупку {message.successful_payment.total_amount // 100} {message.successful_payment.currency}!"
    await message.answer(msg)
    await message.edit_text("Пожалуйста, выбери, что ты хочешь сделать", reply_markup=menu_kb)