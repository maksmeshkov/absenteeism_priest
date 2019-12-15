import subprocess
import requests
import telebot
from telebot import apihelper

token = "771355138:AAErIdt3hlZgu1HHk8BbzfqRK3-vCWBpgic"
bot = telebot.TeleBot(token)

proxy = {'https': "socks5://DHGuCN:BRqGKg@77.83.30.144:8000"}
apihelper.proxy = proxy


def line_has_lesson(line):
    if len(line) >= 10 and line[10:14] != "    ":
        return True
    else:
        return False


def get_absences(username):
    filename = r"files/" + username + "_parsed.txt"
    parsed = open(filename, "r", encoding="UTF-8")

    visits_schedule = {
        # "lesson_name" : amount of skips
    }

    amount_of_visited_lessons = {
        # "lesson_name" : amount of visited lessons
    }

    for line in parsed:
        if "8" >= line[0] >= "1":
            if line_has_lesson(line):
                # lesson_name = line[10:36].strip()
                amount_of_visited_lessons[line[10:36].strip()] = amount_of_visited_lessons.get(line[10:36].strip(),
                                                                                               0) + 1
                if "   н" in line[70:100]:
                    visits_schedule[line[10:36].strip()] = visits_schedule.get(line[10:36].strip(), 0) + 1
            else:
                if "   н" in line[70:100]:
                    visits_schedule[previous_line] = visits_schedule.get(previous_line, 0) + 1
        else:
            if line[0] == " ":
                previous_line = line[10:36].strip()

    return visits_schedule


def parse_file(username):
    # короче вся эта херня будет запускатся на линукс сервере с установленным pdftotext
    pdf_name = r"files/" + username + ".pdf"
    parsed_name = r"files/" + username + "_parsed.txt"
    subprocess.run(["pdftotext", "-layout", str(pdf_name), parsed_name])


def generate_download_link(id):
    link = "https://dnevnik.mos.ru/reports/api/student_journal/pdf?student_profile_id=" + id + "&begin_date=09.09.2019" \
                                                                                               "&end_date=15.12.2019" \
                                                                                               "&scale=five "
    return link


def get_file(message):
    print("SysReport for " + str(message.chat.first_name) + ": initiated get_file sequence")
    if message.document is None:
        bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=B9pBzcUo8aA")
    elif message.document.file_name[-4:] != ".pdf":
        bot.send_message(message.chat.id, "не то шлешь")
    else:
        url = "https://api.telegram.org/bot{}/getFile?file_id={}".format(token, str(message.document.file_id))
        print("SysReport for " + str(message.chat.first_name) + ": got url")
        r = requests.get(url, proxies=proxy)
        print("SysReport for " + str(message.chat.first_name) + ": got requests")
        text = r.text
        file_name = text[(text.rindex(":") + 2):text.rindex("\"")]
        dlink = "https://api.telegram.org/file/bot{}/{}".format(token, file_name)
        download = requests.get(dlink, proxies=proxy, allow_redirects=True)
        dname = r"files/" + message.chat.first_name + ".pdf"
        open(dname, "wb").write(download.content)
        print("SysReport for " + str(message.chat.first_name) + ": got download")


def get_dict(first_name):
    absences = get_absences(first_name)
    return absences



