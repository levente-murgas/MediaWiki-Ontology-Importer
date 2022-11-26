from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import nltk as nltk
import os
import json as js
import re
import hu_core_news_lg
from nltk.corpus import stopwords
import requests
import urllib.parse
import rdflib
import pandas as pd
from bs4 import BeautifulSoup
from rdflib import URIRef, BNode, Literal, Namespace
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO, SKOS

EX = Namespace('http://example.org/')
hungarian_stopwords = stopwords.words('hungarian')
nlp_hu = hu_core_news_lg.load()

dictionary = {}
path = r"C:\Users\Murgi\Documents\GitHub\temalab\fejezetek"
save_to = r"C:\Users\Murgi\Documents\GitHub\temalab\fejezetek_txtben"

def add_file_to_index(path):
    # open the file document that is to be indexed
    file = open(path, encoding='utf8')

    # extract name from file name
    pattern = r".+\\|.txt"
    chapter = re.sub(pattern,'',path)
    read = file.read()
    file.seek(0)

    # read lines into a list
    lines = file.readlines()

    # open vocabulary
    vocab_file = open('filtered_vocab.txt', encoding='utf-8')
    
    # read keywords from vocab to list
    keyword_lines = vocab_file.read().splitlines()
    keywords = []
    for line in keyword_lines:
        keywords.append(line.split(','))

    # iterate over every line of the document and check for every keyword if it contains it
    for i in range(len(lines)):
        check123 = lines[i].lower()
        doc = nlp_hu(lines[i].lower())
        check = ' '.join([token.lemma_ for token in doc if token.lemma_ not in hungarian_stopwords])
        if check.isspace():
            pass
        else:
            for item in keywords:
                for synonym in item:
                    if check.find(synonym) != -1:
                        if item[0] not in dictionary:
                            dictionary[item[0]] =  {}
                            dictionary[item[0]][chapter] = [1, [i+1]]
                        else:
                            if chapter not in dictionary[item[0]]:
                                dictionary[item[0]][chapter] = [1, [i+1]]
                            else:
                                dictionary[item[0]][chapter][1].append(i+1)
                                dictionary[item[0]][chapter][0] +=  1

# recursively index each file in the folder
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


def get_thesaurus():
    df = pd.DataFrame(columns=['Subject','Predicate', 'Object'])

    # open vocabulary
    vocab_file = open('filtered_vocab.txt', encoding='utf-8')
    
    # read keywords from vocab to list
    keyword_lines = vocab_file.read().splitlines()
    keywords = []
    for line in keyword_lines:
        keywords.append(line.split(','))

    for item in keywords:
        for synonym in item:
            query = requests.post(url = f'https://mek.oszk.hu/cgi-bin/thes.cgi?desc={urllib.parse.quote(synonym,encoding="windows-1250")}&trunc=1')
            soup = BeautifulSoup(query.text, 'html.parser')
            last_predicate = ""
            # Collecting Data
            try:
                for row in soup.body.table.find_all('tr'):
                    # Find all data for each column
                    columns = row.find_all('td')
                    if len(columns) > 1 and columns[0].text.strip() != "ETO":
                        curr_predicate = columns[0].text.strip()
                        _object = columns[1].a.text
                        if curr_predicate != "":
                            last_predicate = curr_predicate
                        else:
                            curr_predicate = last_predicate
                        print(synonym,_object,curr_predicate)
                        df = df.append({'Subject': synonym,'Predicate': curr_predicate,'Object': _object},ignore_index=True)
            except: 
                continue

            # print(soup.body.table)
            # for link in soup.body.table.find_all('a')[1:]:
            #     print(link.text)
    return df

def build_rdf():
    g = rdflib.Graph()
    g.bind('skos', SKOS)
    g.bind('ex',EX)

# extract_pdf_to_txt(path,save_to)
# index_file('test')

# add_folder_to_index('fejezetek_txtben')
# serialize_index_to_JSON('index3_with_stemming')

df = get_thesaurus()
print(df.head(20))
# dictionary = deserialize_index_from_JSON('index2_with_synonyms')
# file2 = open("results2.txt", "a", encoding='utf-8') 
# for item in keywords:
#     file2.write(get_occurences(item,'results2'))
# file2.close()

# dictionary = deserialize_index_from_JSON('index3_with_stemming')
# file3 = open('results3.txt','a', encoding='utf-8')
# for item in keywords:
#     file3.write(get_occurences(item,'results3'))
# file3.close()
