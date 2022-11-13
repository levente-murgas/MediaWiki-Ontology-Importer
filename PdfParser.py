from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import re
# from datetime import datetime
# a = datetime.now()
i = 0
path = r"C:\Users\murga\OneDrive\Documents\GitHub\temalab\vocab"
save_to = r"C:\Users\murga\OneDrive\Documents\GitHub\temalab"

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