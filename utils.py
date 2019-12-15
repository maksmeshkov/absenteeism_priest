import os.path
import subprocess

import requests
import telebot
from telebot import apihelper
from telebot import types

from parser import get_absences

token = "956795464:AAE4s0E_0rmwNgEy1gOM8FNAmibuprEyUXU"
bot = telebot.TeleBot(token)
proxy = {'https': "socks5://DHGuCN:BRqGKg@77.83.30.144:8000"}
apihelper.proxy = proxy

startup_msg = """Я выведу количество твоих прогулов за год по каждому предмету. 
Для начала открой в браузере свой дневник на dnevnik.mos.ru, подожди когда загрузится главная страница и отправь мне ссылку на нее. 

Сылка должна иметь вид https://dnevnik.mos.ru/student_diary/student_diary/1234567
"""
help_msg = "Чем тебе помочь?"
error_msg = "Я тебя не понимаю, нажми на кнопку *Помощь*"
again_msg = """
Для начала открой в браузере свой дневник на dnevnik.mos.ru, подожди когда загрузится главная страница и отправь мне ссылку на нее. 

Сылка должна иметь вид   `https://dnevnik.mos.ru/student_diary/student_diary/1234567`

Затем отправь мне файл который открывается у тебя по сгенерированной ссылке и нажми на кнопку *Мои прогулы*
"""


def out_keyboard(message, error=False):
    keyboard = types.ReplyKeyboardMarkup()
    key_help = types.KeyboardButton(text='Помощь')
    keyboard.add(key_help)
    key_print = types.KeyboardButton(text='Мои прогулы')
    keyboard.add(key_print)
    # key_upload = types.KeyboardButton(text='Обработай файл')
    # keyboard.add(key_upload)
    if not error:
        bot.send_message(text=startup_msg, chat_id=message.chat.id, reply_markup=keyboard)
    if error:
        out_error(message)


def out_help(message, error_code="first_call"):
    if error_code == "first_call":
        keyboard = types.InlineKeyboardMarkup()
        key_upload = types.InlineKeyboardButton(text='Обьясни что делать еще раз', callback_data='again')
        keyboard.add(key_upload)
        key_help = types.InlineKeyboardButton(text='Не откывается ссылка', callback_data='link_error')
        keyboard.add(key_help)
        key_print = types.InlineKeyboardButton(text="Не отправляется файл", callback_data='file_error')
        keyboard.add(key_print)
        key_upload = types.InlineKeyboardButton(text='Другая проблема', callback_data='other_error')
        keyboard.add(key_upload)
        bot.send_message(message.chat.id, text=help_msg, reply_markup=keyboard)
    if error_code == "again":
        bot.send_message(message.chat.id, text=again_msg, parse_mode="Markdown")


def out_error(message):
    bot.send_message(message.chat.id, error_msg, parse_mode="Markdown")


def out_dict(message):
    parsed_name = r"files/" + message.chat.first_name + "_parsed.txt"
    pdf_name = r"files/" + message.chat.first_name + ".pdf"
    if os.path.isfile(pdf_name):
        if os.path.isfile(parsed_name):
            formatted_dict = ""
            book = get_dict(message.chat.first_name)
            for k, v in book.items():
                formatted_dict += (str(k) + " - " + str(v) + "\n")
            if formatted_dict != "":
                bot.send_message(message.chat.id, formatted_dict)
            else:
                bot.send_message(message.chat.id, "В загруженном файле не обнаружено расписание.")
        else:
            parse_file(message.chat.first_name)
    else:
        bot.send_message(message.chat.id, "Загрузите ваше расписание прежде чем смотреть его.")


def parse_file(username):
    # короче вся эта херня будет запускатся на линукс сервере с установленным pdftotext
    parsed_name = r"files/" + username + "_parsed.txt"
    pdf_name = r"files/" + username + ".pdf"
    # if not os.path.isfile(parsed_name):  # убарл чтобы можно было новые файлы обрабатывать
    subprocess.run(["pdftotext", "-layout", str(pdf_name), parsed_name])


def get_file(message):
    # if message.document is None:  # убрал эту проверку потому что есть уровнем выше
    #     bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=B9pBzcUo8aA")
    if message.document is None or message.document.file_name[-4:] != ".pdf":
        bot.send_message(message.chat.id, "не то шлешь")
    else:
        url = "https://api.telegram.org/bot{}/getFile?file_id={}".format(token, str(message.document.file_id))
        r = requests.get(url, proxies=proxy)
        text = r.text
        file_name = text[(text.rindex(":") + 2):text.rindex("\"")]
        dlink = "https://api.telegram.org/file/bot{}/{}".format(token, file_name)
        download = requests.get(dlink, proxies=proxy, allow_redirects=True)
        dname = r"files/" + message.chat.first_name + ".pdf"
        open(dname, "wb").write(download.content)
        parse_file(message.chat.first_name)
        bot.send_message(message.chat.id, "Файл обработан, можешь посмотреть свои прогулы)")


def get_dict(first_name):
    absences = get_absences(first_name)
    return absences


def get_dlink(message):
    arch_link = message.text.split("/")
    student_id = arch_link[-1]
    print(student_id)
    from datetime import datetime
    date = datetime.now().strftime('%d.%m.%Y')
    print(date)
    link = "https://dnevnik.mos.ru/reports/api/student_journal" \
           "/pdf?student_profile_id=" + student_id + "&begin_date=01.09.2019&end_date=" + date + "&scale=five "
    support_msg = """
    Отлично!
    Теперь отправь мне файл который открывается у тебя по сгенерированной ссылке: 
    """ + "\n" + link + """

Если у тебя айфон, то просто открой эту ссылку в браузере (если открывать через телеграм то может не открыться:
в таком случае нажми кнопку открыть в браузере) и нажми кнопку поделиться через телеграм со мной.
    """
    bot.send_message(message.chat.id, support_msg)
