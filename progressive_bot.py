import telebot
from telebot import apihelper

from utils import out_keyboard, out_dict, out_help, get_file, get_dlink

token = "   "
bot = telebot.TeleBot(token)
proxy = {'https': "    "}
apihelper.proxy = proxy


@bot.message_handler(commands=["start"])
def start(message):
    out_keyboard(message)


@bot.message_handler(content_types=["text"])
def text_worker(message):
    if message.text == "Помощь":
        out_help(message)
    elif message.text == "Мои прогулы":
        out_dict(message)
    elif message.text[8:15] == "dnevnik":
        get_dlink(message)
    else:
        out_keyboard(message, error=True)


@bot.message_handler(content_types=["document"])
def file_worker(message):
    get_file(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "again":
        out_help(call.message, error_code="again")


bot.polling(none_stop=True)
