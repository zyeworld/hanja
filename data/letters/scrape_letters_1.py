# 나무위키 '전국한자능력검정시험/배정한자' 게시물 참고용 코드
# (8급 - 3급)

import json
from collections import OrderedDict

json_data = OrderedDict()

hanja_data = []
footnotes_data = []

level = '8'

# 나무위키 한자 게시물에서 한자 부분들을 긁어와 저장해야 한다.
# ex) https://namu.wiki/w/전국한자능력검정시험/배정한자/5급
with open(f'namuwiki_data/hanja_{level}.txt') as hanja_file:    
    hanja_data = hanja_file.readlines()

# 동일한 게시물에서 주석을 긁어와 저장해야 한다.
# with open(f'namuwiki_data/footnote_{level}.txt') as footnotes_file:
#     footnotes_data = footnotes_file.readlines()

footnotes_dict = {}
for line in footnotes_data:
    line_split_index = line.find(']')
    footnote_num = line[1:line_split_index]
    footnote_content = line[line_split_index+2:]
    footnotes_dict[footnote_num] = footnote_content

for line in hanja_data:
    # ex) 復 회복할 복 | 다시 부:[11]
    #     ^ letter
    #        ^ huneums(훈음)
    #                            ^ footnote
    hanja_letter = line[0]

    # 주석
    footnotes = []

    footnote_split = line[2:].split('[')
    if len(footnote_split) > 1:
        for footnote in footnote_split[1:]:
            if footnote[:-1] in footnotes_dict:
                footnotes.append(footnotes_dict[footnote[:-1]])
    
    # 훈음
    huneums = str(footnote_split[0]).split('|')
    huneums_clean = []
    for huneum in huneums:
        huneum = huneum.strip()
        split_index = huneum.rfind(' ')
        huneums_clean.append({'hun': huneum[:split_index], 'eum': huneum[split_index+1:]})

    json_data[hanja_letter] = {
        'level': f'{level}',
        'huneum': huneums_clean,
        'words': footnotes
    }

    
with open(f'namuwiki_data/letter_{level}.json', 'w') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=2)
