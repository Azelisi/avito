from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class MyCallBack(CallbackData, prefix="cb"):
    foo: str
    bar: int  

cb_info = MyCallBack(foo='info', bar=1)
cb_return = MyCallBack(foo='return_to_main', bar=1)
cb_pars = MyCallBack(foo='parsing', bar=1)
cb_payment = MyCallBack(foo='pay', bar=1)
cb_tokens_1 = MyCallBack(foo='token', bar=1)
cb_tokens_5 = MyCallBack(foo='token', bar=5)
cb_tokens_10 = MyCallBack(foo='token', bar=10)

how_many_tokens = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= "1 токен", callback_data=MyCallBack(foo='token', bar=1).pack())],
    [InlineKeyboardButton(text= "5 токенов", callback_data=MyCallBack(foo='token', bar=5).pack())], 
    [InlineKeyboardButton(text= "10 токенов", callback_data=MyCallBack(foo='token', bar=10).pack())]
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
