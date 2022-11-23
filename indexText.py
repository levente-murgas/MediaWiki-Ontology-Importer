from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import nltk as nltk
from nltk.tokenize import word_tokenize
import os
import json as js
import re

dictionary = {}
path = r"C:\Users\Murgi\Documents\GitHub\temalab\fejezetek"
save_to = r"C:\Users\Murgi\Documents\GitHub\temalab\fejezetek_txtben"

def add_file_to_index(path):
    file = open(path, encoding='utf8')
    pattern = r".+\\|.txt"
    chapter = re.sub(pattern,'',path)
    read = file.read()
    file.seek(0)
    #read lines into a list
    lines = file.readlines()

    vocab_file = open('filtered_vocab.txt', encoding='utf-8')
    keywords = vocab_file.read().splitlines()

    for i in range(len(lines)):
        check = lines[i].lower()
        if check.isspace():
            pass
        else:
            for item in keywords:
                if check.find(item) != -1:
                    if item not in dictionary:
                        dictionary[item] =  {}
                        dictionary[item][chapter] = [1, [i+1]]
                    else:
                        if chapter not in dictionary[item]:
                            dictionary[item][chapter] = [1, [i+1]]
                        else:
                            dictionary[item][chapter][1].append(i+1)
                            dictionary[item][chapter][0] +=  1

def add_folder_to_index(foldername):
    for filename in os.listdir(foldername):
        if os.path.isdir(filename):
            add_folder_to_index(filename)
        else:
            if filename.endswith(".txt"):
                add_file_to_index(f'{foldername}\{filename}')


def serialize_index_to_JSON(filename):
    # create json object from dictionary
    json = js.dumps(dictionary,indent=2, ensure_ascii=False)
    # open file for writing, "w" 
    f = open(f"{filename}.json","w", encoding='utf8')
    # write json object to file
    f.write(json)
    # close file
    f.close()

def deserialize_index_from_JSON(filename):
    # opening JSON file
    with open(f'{filename}.json', encoding='utf8') as json_file:
        return js.load(json_file)

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
            with open(save_to+"\\"+filename+".txt", "w", encoding="utf-8") as text_file:
                text_file.write(string)
            i = i+1

def get_occurences(keyword):
    cnt = 0
    result = dictionary.get(keyword)
    if result is None:
        print(f'{keyword} : {cnt}')
    else:
        # print(result)
        for value in result.values():
            cnt += value[0]
        print(f'{keyword} : {cnt}')

# extract_pdf_to_txt(path,save_to)
# index_file('test')
# dictionary = deserialize_index_from_JSON('index1')

add_folder_to_index('fejezetek_txtben')
serialize_index_to_JSON('index1')

vocab_file = open('filtered_vocab.txt', encoding='utf-8')
keywords = vocab_file.read().splitlines()
for item in keywords:
    get_occurences(item)

#print(dictionary)



