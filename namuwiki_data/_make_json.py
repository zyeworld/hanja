import json
from collections import OrderedDict

json_data = OrderedDict()

hanja_data = []
words_data = []

level = '1'

with open(f'namuwiki_data/hanja_{level}.txt') as hanja_file:    
    hanja_data = hanja_file.readlines()

with open(f'namuwiki_data/words_{level}.txt') as words_file:
    words_data = words_file.readlines()

words_dict = {}
for line in words_data:
    line_split_index = line.find(']')
    footnote_num = line[1:line_split_index]
    footnote_content = line[line_split_index+2:]
    words_dict[footnote_num] = footnote_content

for key in words_dict:
    print(words_dict[key])
    break

i = 0
while i < len(hanja_data):
    hanja_cur = hanja_data[i].strip()
    meanings = []
    i += 1
    while i < len(hanja_data) and len(hanja_data[i].strip()) > 1:
        meanings.append(hanja_data[i].strip())
        i += 1
    
    footnotes = []
    for meaning in meanings:
        footnote_split = meaning.split('[')
        for footnote in footnote_split[1:]:
            if footnote[:-1] in words_dict:
                footnotes.append(words_dict[footnote[:-1]])
    
    meanings_clean = []
    for meaning in meanings:
        meaning = meaning.split('[')[0]
        split_index = meaning.rfind(' ')
        meanings_clean.append({'hun': meaning[:split_index], 'eum': meaning[split_index+1:]})
    
    json_data[hanja_cur] = {
        'level': f'{level}',
        'huneum': meanings_clean,
        'words': footnotes
    }
    
with open(f'namuwiki_data/list_{level}.json', 'w') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=2)
