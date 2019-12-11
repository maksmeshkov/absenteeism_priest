def generate_download_link(id):
    link = "https://dnevnik.mos.ru/reports/api/student_journal/pdf?student_profile_id=" + id + "&begin_date=09.12.2019" \
                                                                                           "&end_date=15.12.2019" \
                                                                                           "&scale=five "
    return link
