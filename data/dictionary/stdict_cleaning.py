import csv

rows = [['표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례']]

with open('data/dictionary/stdict.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    head = True
    for row in reader:
        if head:
            head = False
            continue
        
        # '어휘', '원어', '원어·어종', '품사', '뜻풀이', '용례', '속담', '관용구'
        #  0       1       2             3       4         5       6       7
        
        # 원어가 한자 아니면 건너뛰기
        if '한자' not in row[2]:
            continue

        # 용례 비었으면 건너뛰기
        if len(row[5].strip()) <= 4:
            continue
        
        # 어휘 -> 표제어 + 동형어 번호 나누기
        # 가격(01) -> 가격, 1
        homonym_num = ''
        word_name = row[0]
        if '(' in word_name:
            word_name_temp = word_name.split('(')
            word_name = word_name_temp[0]

            homonym_num = word_name_temp[1].split(')')[0]
            homonym_num = str(int(homonym_num)) # 0 지우기

        # 양식 바꾸기
        new_row = [word_name, homonym_num, row[1], row[3], row[4], row[5]]
        # '표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례',
        #  0         1               2       3       4         5

        # strip
        new_row = [text.strip() for text in new_row]

        # 표제어에서 기호 빼기
        new_row[0] = new_row[0].translate({ord(char): None for char in '-^'})

        # 원어에서 스페이스바, 사전 기호 지우기
        new_row[2] = new_row[2].translate({ord(char): None for char in ' ▽▼'})

        # 품사, 뜻풀이, 용례에서 "[Ⅰ]「1」" => "Ⅰ|1|" 꼴로 줄이기 (사전에 |가 등장하지 않는 것 활용)
        new_row[3] = new_row[3].translate({ord('「'): None, ord('」'): None, ord('['): None, ord(']'): '|'})
        new_row[4] = new_row[4].translate({ord('「'): None, ord('」'): '|', ord('['): None, ord(']'): '|'})
        new_row[5] = new_row[5].translate({ord('「'): None, ord('」'): '|', ord('['): None, ord(']'): '|'})

        # 품사 절약
        new_row[3] = new_row[3].replace('사', '')

        # 뜻풀이 절약
        meaning_list = new_row[4].split('\n')
        for meaning in meaning_list:
            if meaning[-1] == '.':
                meaning = meaning[:-1]
        new_row[4] = '\n'.join(meaning_list)

        # 용례 절약
        example_list = new_row[5].split('\n')
        example_list.sort(key= lambda x: len(x), reverse= True)
        new_row[5] = '\n'.join(example_list[:3])
        new_row[5] = new_row[5].replace('≫', '')

        rows.append(new_row)

print(len(rows))

# with open('data/dictionary/stdict_clean.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(rows)

