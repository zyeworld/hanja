# letter_*.json 파일 만든 뒤 글자 리스트 뽑기.

import json

levels = ['8', '7p', '7', '6p', '6', '5p', '5', '4p', '4', '3p', '3', '2', '1', '0p', '0']
# 'p' = '준'. '0' = 특급.

hanjas = []

for level in levels:
    with open(f'data/letters/letter_{level}.json', 'r') as file:
        data = json.load(file)
        
        print(level, len(data))
        
        for key in data:
            hanjas.append(key)

with open('data/letters/letter_list.txt', 'w') as file:
    file.write(''.join(hanjas))