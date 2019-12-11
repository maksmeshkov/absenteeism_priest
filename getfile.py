import subprocess


def getfile(pdf_name):
    # короче вся эта херня будет запускатся на линукс сервере с установленным pdftotext
    subprocess.run(["pdftotext", "-layout", str(pdf_name), "parsed.txt"])
    return 'parsed.txt'

