from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import flags

from src.config.cfg import bot
from src.keyboards.inline import menu_kb, return_to_main_kb, how_many_day_sub_banks, how_many_day_sub_crypt, \
    MyCallBack, type_of_payment
from src.handlers.cryptomus import create_invoice
from src.parser.database import get_all_ads

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


# В глобальной области видимости определите структуру данных для хранения уже отправленных уведомлений
sent_notifications = {}
is_running = False


async def parse_and_send_notifications(user_id):
    global is_running
    is_running = True
    while is_running:
        await asyncio.sleep(2)  # 3600 секунд = 1 час
        # Выполняем парсинг
        new_ad_text = get_all_ads()

        # Проверяем, было ли уже отправлено такое уведомление для данного пользователя
        ad_text = new_ad_text[0][1]  # Предполагаем, что текст объявления находится во втором элементе кортежа
        formatted_message = format_message(ad_text)  # Форматируем текст объявления

        if user_id not in sent_notifications:
            sent_notifications[user_id] = set()

        if formatted_message not in sent_notifications[user_id]:
            # Отправляем уведомление
            await bot.send_message(user_id, formatted_message, parse_mode="HTML")
            # Добавляем отправленное уведомление в список уже отправленных для данного пользователя
            sent_notifications[user_id].add(formatted_message)

        # Ждем некоторое время перед следующим парсингом
        print(is_running)
        await asyncio.sleep(3)


def format_message(ad_text):
    # Функция для форматирования текста объявления с использованием HTML-тега <b>
    format_text = ad_text.split('\n')
    return "<b>" + "</b>\n<b>".join(format_text) + "</b>"


@router.message(F.text.lower().strip() == 'стоп')
async def stop_pars(message: Message):
    global is_running
    user_id = message.from_user.id
    if user_id in sent_notifications:
        del sent_notifications[user_id]  # Удаляем все отправленные уведомления для пользователя
        is_running = False  # Это необходимо, чтобы парсер перестал запускаться для всех пользователей
    await message.reply("Парсер остановлен 😴")


# Роутер парсинга..
# Проверка в базе на то что пользователь подписан (то есть, смотрим в базу данных user_id и sub_status и если sub_status равен 1 то всё заебисб)
@router.callback_query(MyCallBack.filter(F.foo == 'parsing'))
async def start_process_of_pars(query: types.CallbackQuery, callback_data: MyCallBack):
    global is_running
    user_id = query.from_user.id
    print(f"Start parsing cycle for user {user_id}, {query.data}")

    # Отправляем уведомление о начале парсинга
    await query.message.answer(
        "Парсинг запущен 🚀\nТы будешь получать уведомления о новых объявлениях\n\nДля остановки напиши - <b>Стоп</b>",
        parse_mode="HTML")
    # Запускаем асинхронную функцию, которая будет выполнять парсинг и отправлять уведомления
    await asyncio.create_task(parse_and_send_notifications(user_id))
    if not is_running:
        await query.message.answer("Парсер остановлен 😴", reply_markup=menu_kb)
