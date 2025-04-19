import csv
import json

csv_filename = 'data/dictionary/krdict_clean.csv'
json_filename = 'data/dictionary/krdict.json'
json_data = []

with open(csv_filename, newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    head = True
    for row in reader:
        if head:
            head = False
            continue
        # '표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례',
        #  0         1               2       3       4         5
        json_data.append({
            'w': row[0] + row[1], # word
            'o': row[2], # original
            'c': row[3], # class
            'm': row[4], # meaning
            'e': row[5] # example
        })

json_str = json.dumps(json_data, ensure_ascii=False, indent=0, separators=(',', ':'))
with open(json_filename, 'w') as file:
    file.write(json_str)
