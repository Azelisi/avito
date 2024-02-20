from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class MyCallBack(CallbackData, prefix="cb"):
    foo: str
    bar: int  

cb_info = MyCallBack(foo='info', bar=1)
cb_return = MyCallBack(foo='return_to_main', bar=1)
cb_pars = MyCallBack(foo='parsing', bar=1)
cb_payment = MyCallBack(foo='pay', bar=1)
cb_sub_7 = MyCallBack(foo='sub', bar=7)
cb_sub_14 = MyCallBack(foo='sub', bar=14)
cb_sub_30 = MyCallBack(foo='sub', bar=30)

how_many_day_sub = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= "7 дней", callback_data=MyCallBack(foo='sub', bar=7).pack())],
    [InlineKeyboardButton(text= "14 дней", callback_data=MyCallBack(foo='sub', bar=14).pack())], 
    [InlineKeyboardButton(text= "30 дней", callback_data=MyCallBack(foo='sub', bar=30).pack())],
    [InlineKeyboardButton(text= "Назад", callback_data=MyCallBack(foo='return_to_main', bar=1).pack())]
])

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= "Начать парс", callback_data=MyCallBack(foo='parsing', bar=1).pack())],
    [InlineKeyboardButton(text= "Пополнить баланс", callback_data=MyCallBack(foo='pay', bar=1).pack())], 
    [InlineKeyboardButton(text= "Инфо", callback_data=MyCallBack(foo='info', bar=1).pack())]
])

return_to_main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= "Назад", callback_data=MyCallBack(foo='return_to_main', bar=1).pack())]
])

payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= "Пополнить", callback_data=MyCallBack(foo='pay', bar=1).pack())],
    [InlineKeyboardButton(text= "Назад", callback_data=MyCallBack(foo='return_to_main', bar=1).pack())]
])
