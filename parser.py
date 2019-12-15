import subprocess


def line_has_lesson(line):
    if len(line) >= 10 and line[10:14] != "    ":
        return True
    else:
        return False


def get_absences(username):
    filename = r"files/" + username + "_parsed.txt"
    parsed = open(filename, "r", encoding="UTF-8")
    previous_line = ""
    visits_schedule = {
        # "lesson_name" : amount of skips
    }

    total_lessons = {
        # "lesson_name" : total amount of lessons
    }

    for line in parsed:
        if "8" >= line[0] >= "1":
            if line_has_lesson(line):
                total_lessons[line[10:36].strip()] = total_lessons.get(line[10:36].strip(), 0) + 1
                if "   н" in line[70:100]:
                    visits_schedule[line[10:36].strip()] = visits_schedule.get(line[10:36].strip(), 0) + 1
            else:
                if "   н" in line[70:100]:
                    visits_schedule[previous_line] = visits_schedule.get(previous_line, 0) + 1
        else:
            if line[0] == " ":
                previous_line = line[10:36].strip()

    return visits_schedule, total_lessons


def parse_file(username):
    # короче вся эта херня будет запускатся на линукс сервере с установленным pdftotext
    pdf_name = r"files/" + username + ".pdf"
    parsed_name = r"files/" + username + "_parsed.txt"
    subprocess.run(["pdftotext", "-layout", str(pdf_name), parsed_name])
