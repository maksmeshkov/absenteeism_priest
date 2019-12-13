import telebot
# from telebot import apihelper
import wget
import requests

import linkgen

import main

token = "827444038:AAHO0cnALFCTMa6cYhaSt1NDh2YdIyCACPo"
bot = telebot.TeleBot(token)
# apihelper.proxy = {'http': "socks5://DHGuCN:BRqGKg@77.83.30.144:8000"} тут надо как-то настроить прокси
book = {'Русский язык': 17, 'Литература': 16, 'Физика': 31, 'Иностранный язык': 24, 'Геометрия': 14, 'Алгебра и начала': 28, 'Индивидуальный проект': 5, 'Физическая культура': 15, 'Химия': 4, 'Информатика': 20, 'Астрономия': 7, 'История': 13, 'Биология': 5, 'Колебания и волны в': 2, 'Основы безопасности': 1}


@bot.message_handler(commands=["start"])
def start(mes):
    bot.send_message(mes.chat.id, "Отправь мне ссылку из своего дневника, выглядеть должно так: https://dnevnik.mos.ru/student_diary/student_diary/123456")
    bot.register_next_step_handler(mes, generate_a_link)

def generate_a_link(message):
    try:
        recieved_link = message.text
        id = recieved_link[recieved_link.rindex("/") + 1 : ]
        try:
            int(id)
        except:
            msg = bot.send_message(message.chat.id, 'Введите правильную ссылку')
            bot.register_next_step_handler(msg, generate_a_link)
            return
        link = linkgen.generate_download_link(id)
        bot.send_message(message.chat.id,"Перейдите по этой ссылке и скачайте файл: "+ link)
    except:
        msg = bot.send_message(message.chat.id, 'Введите правильную ссылку')
        bot.register_next_step_handler(msg, generate_a_link)
        return

#вывод словаря
@bot.message_handler(commands=["out"])
def output(mes):
    striga = ""
    for k, v in book.items():
        striga += k
        striga += " - "
        striga += str(v)
        striga += ("\n")
    bot.send_message(mes.chat.id, striga)

@bot.message_handler(commands=["get"])
def wait_for_a_file(mes):
    msg = bot.send_message(mes.chat.id,"Пришлите файл с оценками")
    bot.register_next_step_handler(msg,get_file)


def get_file(message):
    url = "https://api.telegram.org/bot{}/getFile?file_id={}".format(token,str(message.document.file_id))
    r = requests.get(url)
    text = r.text
    file_name = text[(text.rindex(":") + 2):text.rindex("\"")]

    wget.download("https://api.telegram.org/file/bot{}/{}".format(token,file_name))



bot.polling(none_stop=True)