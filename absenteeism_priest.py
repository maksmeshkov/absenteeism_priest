from linkgen import generate_download_link
from getfile import getfile
from main import get_absences

student_id = input("your student id:")
d_link = generate_download_link(student_id)
print("download pdf from this link:", d_link)
# somehow upload pdf into project directory and get its name....
pdf_name = "dnevnik.pdf"
parsed_name = getfile(pdf_name)
print(get_absences())

