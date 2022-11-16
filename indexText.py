import string
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

file = open('test.txt', encoding='utf8')
read = file.read()
file.seek(0)

# count number
# of lines in text 
line = 1
for word in read:
    if word == '\n':
        line += 1
print("Number of lines in file is: ", line)

# create a list to
# store each line as
# an element of list
array = []
for i in range(line):
    array.append(file.readline())

# get rid of punctuations in text
punctuations = list(string.punctuation)
for element in read:
    if element in punctuations:
        read = read.replace(element, " ")
read=read.lower()

stop_words = set(stopwords.words('hungarian'))
word_tokens = word_tokenize(read)
print(word_tokens)
print()
filtered_words = []
  
for w in word_tokens:
    if w not in stop_words:
        filtered_words.append(w)
print(filtered_words)
print()

dict = {}
for i in range(line):
    check = array[i].lower()
    for item in filtered_words:
        if item in check:
            if item not in dict:
                dict[item] = [1]
            if item in dict:
                dict[item].append(i+1)
                num_of_appearances = len(dict[item]) - 1
                dict[item].insert(0,num_of_appearances + 1)

print(dict)