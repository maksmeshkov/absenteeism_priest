import subprocess


def line_has_lesson(line):
    if len(line) >= 10 and line[10:14] != "    ":
        return True
    else:
        return False


def get_absences(username):
    filename = r"./files/" + username + "_parsed.txt"
    parsed = open(filename, "r", encoding="UTF-8")
    previous_line = ""
    stripped_line = ""
    visits_schedule = {
        # "lesson_name" : amount of skips
    }

    total_lessons = {
        # "lesson_name" : total amount of lessons
    }

    for line in parsed:
        if "8" >= line[0] >= "1":
            if line_has_lesson(line):
                stripped_line_list = line[10:36].lstrip().split(" ")[0:3]
                stripped_line = ""
                for el in stripped_line_list:
                    stripped_line += el + " "
                stripped_line = stripped_line.strip()
                total_lessons[stripped_line] = total_lessons.get(stripped_line, 0) + 1
                if "   н" in line[70:100]:
                    visits_schedule[stripped_line] = visits_schedule.get(stripped_line, 0) + 1
            else:
                total_lessons[previous_line] = total_lessons.get(previous_line, 0) + 1
                if "   н" in line[70:100]:
                    visits_schedule[previous_line] = visits_schedule.get(previous_line, 0) + 1
        else:
            if line[0] == " ":
                previous_line_list = line[10:36].lstrip().split(" ")[0:3]
                previous_line = ""
                for el in previous_line_list:
                    previous_line += el + " "
                previous_line = previous_line.strip()
    return visits_schedule, total_lessons


def parse_file(username):
    # короче вся эта херня будет запускатся на линукс сервере с установленным pdftotext
    pdf_name = r"./files/" + username + ".pdf"
    parsed_name = r"./files/" + username + "_parsed.txt"
    subprocess.run(["pdftotext", "-layout", str(pdf_name), parsed_name])
