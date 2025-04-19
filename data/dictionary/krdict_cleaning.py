import csv

def is_hanja(char):
    return (0x3400 <= ord(char) <= 0x4DBF) or \
           (0x4E00 <= ord(char) <= 0x9FFF) or \
           (0xF900 <= ord(char) <= 0xFAFF) or \
           (0x20000 <= ord(char) <= 0x2A6DF) or \
           (0x2A700 <= ord(char) <= 0x2EE5F) or \
           (0x30000 <= ord(char) <= 0x323AF)

rows = [['표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례']]

with open('data/dictionary/krdict.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    head = True
    for row in reader:
        if head:
            head = False
            continue
        
        # '표제어', '동형어 번호', '구분', '품사', '고유어 여부', '원어', '발음', '어휘 등급', '뜻풀이', '용례'
        #  0         1              2       3        4             5       6       7            8         9

        # 용례 비었으면 건너뛰기
        if len(row[9].strip()) <= 4:
            continue
        
        # 원어에 한자 없으면 건너뛰기
        has_hanja = False
        for char in row[5]:
            if is_hanja(char):
                has_hanja = True
                break
        if not has_hanja:
            continue

        # 양식 바꾸기
        new_row = [row[0], row[1], row[5], row[3], row[8], row[9]]
        # '표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례'
        #  0         1              2        3      4         5

        # strip
        new_row = [text.strip() for text in new_row]

        # 용례에서 문장만 남기기
        usage = new_row[5].split('\n')
        
        usage = [x for x in usage if '<문장>' in x]
        if len(usage) == 0:
            usage = new_row[5].split('\n')
            usage = [x for x in usage if '<구>' in x]
        
        if len(usage) == 0:
            continue
        
        # 용례 앞부분 지우기
        usage = [x.replace('<문장> ', '').replace('<구> ', '').strip() for x in usage]
        # 용례 따옴표 바꾸기
        usage = [x.replace('\"', '\'') for x in usage]

        usage.sort(key=lambda x: len(x), reverse=True)

        new_row[5] = '\n'.join(usage[:3])

        # 동형어 번호 0 지우기
        if new_row[1] == '0':
            new_row[1] = ''

        # 원어에서 스페이스바, 사전 기호 지우기
        new_row[2] = new_row[2].translate({ord(char): None for char in ' ▽▼'})

        # 품사 크기 절약
        new_row[3] = new_row[3].replace('사', '')

        # 뜻풀이 크기 절약
        if new_row[4][-1] == '.':
            new_row[4] = new_row[4][:-1]

        rows.append(new_row)
        
print(len(rows))

with open('data/dictionary/krdict_clean.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)