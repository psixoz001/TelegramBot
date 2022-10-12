from telebot import types
from config import *
cat_but=list(category.keys())
def anyButtons(names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in names:  
        markup.add(types.KeyboardButton(name))
    return markup