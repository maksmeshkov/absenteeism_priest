def line_has_lesson(line):
    if len(line) >= 10 and line[10:14] != "    ":
        return True
    else:
        return False


def get_absences():
    parsed = open("parsed.txt", "r")

    visits_schedule = {
        # "lesson_name" : amount of skips
    }

    for line in parsed:
        if "8" >= line[0] >= "1":
            if line_has_lesson(line):
                if "   н" in line[70:100]:
                    visits_schedule[line[10:36].strip()] = visits_schedule.get(line[10:36].strip(), 0) + 1
            else:
                if "   н" in line[70:100]:
                    visits_schedule[previous_line] = visits_schedule.get(previous_line, 0) + 1
        else:
            if line[0] == " ":
                previous_line = line[10:36].strip()
    return visits_schedule


