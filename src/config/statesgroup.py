from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from src.config.cfg import bot
from src.config.statesgroup import MainStateGroup, ParsingAvito
from src.keyboards.inline import menu_kb, return_to_main_kb, payment_kb, how_many_day_sub, MyCallBack
from src.parser.parser import pars


import random
import asyncio

async def timer_db(): 
    while True: 
        asyncio.sleep(60*60*12) # ОБновление каждые 12 часов 
        ###
        ### Берем из бд 
        ###

        ### 
        ### МЕНЯЕМ USER_SUBTIME 
        ###

        ### 
        ### Возвращаем до бд 
        ###