import csv

with open('data/dictionary/stdict_clean.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    head = True
    for row in reader:
        if head:
            head = False
            continue
        # '표제어', '동형어 번호', '원어', '품사', '뜻풀이', '용례',
        #  0         1               2       3       4         5
        
        if '[' in row[2]:
            continue

        has_eng = False
        for char in row[2]:
            if ord('a') <= ord(char) <= ord('z'):
                has_eng = True
                break
        
        if has_eng:
            continue

        if len(row[0]) != len(row[2]):
            print(row[0], row[2])
        