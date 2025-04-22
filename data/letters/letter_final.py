import json
import csv

dict_filename = 'data/dictionary/stdict_clean.csv'
letter_filenames = [f'data/letters/letter_{x}.json' for x in ['8', '7p', '7', '6p', '6', '5p', '5', '4p', '4', '3p', '3', '2', '1', '0p', '0']]
dump_filename = 'data/letters/stdict_letters.json'

hanja_data = [] # {'c':character, 'l': level, 'h': huneum, 'd': dictionary appearances}
hanja_to_num = {}

hanja_index = 0
for filename in letter_filenames:
    with open(filename, 'r') as file:
        content = json.loads(file.read())

        for hanja in content:
            hanja_to_num[hanja] = hanja_index
            hanja_index += 1

            # "校": {
            #     "level": "8",
            #     "huneum": [{"hun": "학교","eum": "교:"}],
            #     "words": []
            # }
            huneums_new = []
            huneums = content[hanja]["huneum"]
            for h in huneums:
                huneums_new.append(h["hun"] + ' ' + h["eum"][0])

            hanja_data.append({
                'c': hanja, # character
                'l': content[hanja]["level"], # level
                'h': huneums_new,
                'd': [], # dictionary appearance indexes
            })


# "d" 필드 채우기
with open(dict_filename, newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    head = True
    index = -1
    for row in reader:
        if head:
            head = False
            continue
        index += 1
        # '표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례',
        #  0         1               2       3       4         5

        # TODO: 표제어와 원어 길이 다를 경우 다루기
        if len(row[0]) != len(row[2]):
            continue
        
        # 원어에서 찾은 한자 각각에 대해 json_data의 'kd' 또는 'sd'에 현재 번호 추가
        for char in row[2]: 
            if char not in hanja_to_num:
                continue
            hanja_index = hanja_to_num[char]
            if index not in hanja_data[hanja_index]["d"]:
                hanja_data[hanja_index]["d"].append(index)

# "d" 필드 빈 것들 없애기
hanja_data = [x for x in hanja_data if len(x['d']) > 0]
# 각 급수 마지막 인덱스 적기 (그냥 매번 업데이트하는 방식으로 함)
level_data = {}
for i in range(len(hanja_data)):
    level_data[hanja_data[i]['l']] = i

json_data = {'level_list': level_data, 'hanja_list': hanja_data}

json_str = json.dumps(json_data, ensure_ascii=False, indent=0, separators=(',', ':'))
with open(dump_filename, 'w') as file:
    file.write(json_str)
