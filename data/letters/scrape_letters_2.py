# 나무위키 '전국한자능력검정시험/배정한자' 게시물 참고용 코드
# (2급 - 특급)

import json
from collections import OrderedDict

json_data = OrderedDict()

hanja_data = []
footnotes_data = []

level = '1'

# 나무위키 한자 게시물에서 한자 부분들을 긁어와 저장해야 한다.
# ex) https://namu.wiki/w/전국한자능력검정시험/배정한자/1급
with open(f'namuwiki_data/hanja_{level}.txt') as hanja_file:    
    hanja_data = hanja_file.readlines()

# 동일한 게시물에서 주석을 긁어와 저장해야 한다.
with open(f'namuwiki_data/footnote_{level}.txt') as footnotes_file:
    footnotes_data = footnotes_file.readlines()

footnotes_dict = {}
for line in footnotes_data:
    line_split_index = line.find(']')
    footnote_num = line[1:line_split_index]
    footnote_content = line[line_split_index+2:]
    footnotes_dict[footnote_num] = footnote_content

i = 0
while i < len(hanja_data):
    hanja_cur = hanja_data[i].strip()
    huneums = []
    i += 1
    while i < len(hanja_data) and len(hanja_data[i].strip()) > 1:
        huneums.append(hanja_data[i].strip())
        i += 1
    
    footnotes = []
    for huneum in huneums:
        footnote_split = huneum.split('[')
        for footnote in footnote_split[1:]:
            if footnote[:-1] in footnotes_dict:
                footnotes.append(footnotes_dict[footnote[:-1]])
    
    meanings_clean = []
    for huneum in huneums:
        huneum = huneum.split('[')[0]
        split_index = huneum.rfind(' ')
        meanings_clean.append({'hun': huneum[:split_index], 'eum': huneum[split_index+1:]})
    
    json_data[hanja_cur] = {
        'level': f'{level}',
        'huneum': meanings_clean,
        'words': footnotes
    }
    
with open(f'namuwiki_data/letter_{level}.json', 'w') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=2)
