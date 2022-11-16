file = open('test.txt', encoding='utf8')
read = file.read()
file.seek(0)
#read lines into a list
lines = file.readlines()

vocab_file = open('filtered_vocab.txt', encoding='utf-8')
keywords = vocab_file.read().splitlines()

dictionary = {}
for i in range(len(lines)):
    check = lines[i].lower()
    if check.isspace():
         pass
    else:
        for item in keywords:
            if check.find(item) != -1:
                if item not in dictionary:
                    dictionary[item] = [1,i+1]
                else:
                    dictionary[item].append(i+1)
                    dictionary[item][0] +=  1
                    
print(dictionary)