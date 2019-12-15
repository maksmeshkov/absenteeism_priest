import telebot
import requests
from telebot import apihelper
from telebot import types
from utils import parse_file
from utils import get_absences
from utils import get_file
from utils import get_dict
from utils import generate_download_link

token = "771355138:AAErIdt3hlZgu1HHk8BbzfqRK3-vCWBpgic"
bot = telebot.TeleBot(token)
proxy = {'https': "socks5://DHGuCN:BRqGKg@77.83.30.144:8000"}
apihelper.proxy = proxy
help_file = "помощь потом допишу, если совсем непонятно, ругай @targetable (сюда линкген привязать)"


@bot.message_handler(commands=["start"])
def start(message):
    # bot.send_message(message.chat.id,
    #                  "Отправь мне ссылку из своего дневника, выглядеть должно так: "
    #                  "https://dnevnik.mos.ru/student_diary/student_diary/123456")
    # bot.register_next_step_handler(message, generate_a_link)
    keyboard = types.InlineKeyboardMarkup()
    key_help = types.InlineKeyboardButton(text='Помощь', callback_data='help')
    keyboard.add(key_help)
    key_print = types.InlineKeyboardButton(text='Мои прогулы', callback_data='get_absents')
    keyboard.add(key_print)
    key_upload = types.InlineKeyboardButton(text='Загрузить файл', callback_data='upload_pdf')
    keyboard.add(key_upload)
    bot.send_message(message.from_user.id, text='Выбери действие', reply_markup=keyboard)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "help":
        keyboard = types.InlineKeyboardMarkup()
        key_return = types.InlineKeyboardButton(text='Назад', callback_data='return')
        keyboard.add(key_return)
        bot.edit_message_text(text=help_file, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=keyboard)

    if call.data == "get_absents":
        try:
            parsed_name = r"files/" + call.message.chat.first_name + "_parsed.txt"
            parsed_file = open(parsed_name)  # 9000 iq проверка на наличие файла без импортирования os модуля
            parsed_file.close()
            formatted_dict = ""
            book = get_dict(call.message.chat.first_name)
            for k, v in book.items():
                formatted_dict += k
                formatted_dict += " - "
                formatted_dict += str(v)
                formatted_dict += "\n"
            if formatted_dict != "":
                bot.send_message(call.message.chat.id, formatted_dict)
            else:
                bot.send_message(call.message.chat.id, "В загруженном файле не обнаружено расписание")
        except IOError:
            bot.send_message(call.message.chat.id, "Ваш файл с оценками не найден, для начала загрузите его")
    if call.data == "upload_pdf":
        keyboard = types.InlineKeyboardMarkup()
        key_return = types.InlineKeyboardButton(text='Отмена', callback_data='return')
        keyboard.add(key_return)
        msg = bot.edit_message_text(text="Присылай pdf который по ссылке скачал", chat_id=call.message.chat.id,
                                    message_id=call.message.message_id, reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_file)
        print("SysReport for " + str(call.message.chat.first_name) + ": got trigger")

        parse_file(call.message.chat.first_name)
        print("SysReport for " + str(call.message.chat.first_name) + ": got parsed")
    if call.data == "return":
        keyboard = types.InlineKeyboardMarkup()
        key_help = types.InlineKeyboardButton(text='Помощь', callback_data='help')
        keyboard.add(key_help)
        key_print = types.InlineKeyboardButton(text='Мои прогулы', callback_data='get_absents')
        keyboard.add(key_print)
        key_upload = types.InlineKeyboardButton(text='Загрузить файл', callback_data='upload_pdf')
        keyboard.add(key_upload)
        bot.edit_message_text(text="Chose your trainer", chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=keyboard)


bot.polling(none_stop=True)
