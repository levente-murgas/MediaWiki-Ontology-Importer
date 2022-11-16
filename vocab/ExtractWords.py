import re 

definition_regex = r"\(D\)([^:]+):"

with open('vocab.txt', 'r', encoding= 'utf-8') as file:
    data = file.read().replace('\n', '')

definitions = re.findall(definition_regex, data)

with open(r'filtered_vocab.txt', 'w', ) as fp:
    for d in definitions:
        d = d.strip().lower()
        # write each item on a new line
        fp.write("%s\n" % d)