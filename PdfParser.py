from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from quntoken import tokenize
from hunspell import Hunspell
import string
import os
import requests
import re
# from datetime import datetime
# a = datetime.now()
path = r"C:\Users\murga\OneDrive\Documents\GitHub\temalab\test"
save_to = r"C:\Users\murga\OneDrive\Documents\GitHub\temalab\test"

def extract_pdf_to_txt(path,save_to):
    i = 0
    for filename in os.listdir(path):
        if filename.endswith(".pdf"):
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            fp = open(path+"\\"+filename,'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            caching = True
            pagenos=set()
            for page in PDFPage.get_pages(fp, pagenos, password=password,caching=caching, check_extractable=True):
                interpreter.process_page(page)
            fp.close()
            device.close()
            string = retstr.getvalue()
            retstr.close()
            #print(string)
            with open(save_to+"\\"+filename+".txt", "w", encoding="utf-8") as text_file:
                text_file.write(string)
            i = i+1
            print(i)
    return filename

def read_file_to_str(filename):
    file = open(filename,"r", encoding="utf-8")
    data = file.read().replace('\n', '')
    return data

# URL_1 = "https://cgit.freedesktop.org/libreoffice/dictionaries/tree/hu_HU/hu_HU.dic"
# response = requests.get(URL_1)
# open("hu_HU.dic", "wb").write(response.content)

# URL_2 = "https://cgit.freedesktop.org/libreoffice/dictionaries/tree/hu_HU/hu_HU.aff"
# response = requests.get(URL_2)
# open("hu_HU.aff", "wb").write(response.content)


stemmer = Hunspell('hu_HU', system_encoding='UTF-8').stem

# filename = extract_pdf_to_txt(path,save_to)

text_str = read_file_to_str('test.txt')

for tok in tokenize(iter(text_str)):
    print(tok, end='')

# TODO: restart PC so PATH file updates, fix encoding issue.