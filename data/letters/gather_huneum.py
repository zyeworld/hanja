import json

letter_filenames = [f'data/letters/letter_{x}.json' for x in ['8', '7p', '7', '6p', '6', '5p', '5', '4p', '4', '3p', '3', '2', '1', '0p', '0']]
dump_filename = 'data/letters/huneum.json'

huneum_data = {} # {'가': [ {'h': '집': 'c': '家'} , ...] }

for filename in letter_filenames:
    with open(filename, 'r') as file:
        content = json.loads(file.read())

        for hanja in content:
            # "校": {
            #     "level": "8",
            #     "huneum": [{"hun": "학교","eum": "교:"}],
            #     "words": []
            # }
            huneums = content[hanja]["huneum"]
            for h in huneums:
                hun = h["hun"]
                eum = h["eum"][0]
                if eum not in huneum_data:
                    huneum_data[eum] = []

                # '가': [ {'h': '집': 'c': '家'} , ...] 꼴 만들기
                already_exist = False
                for hun_dict in huneum_data[eum]:
                    if hun_dict['h'] == hun:
                        already_exist = True
                        hun_dict['c'] += hanja # 같은 훈음의 한자가 두 개 이상이면 그냥 'c'에 추가
                if not already_exist:
                    huneum_data[eum].append({
                        'h': hun,
                        'c': hanja
                    })

json_str = json.dumps(huneum_data, ensure_ascii=False, indent=0, separators=(',', ':'), sort_keys=True)
with open(dump_filename, 'w') as file:
    file.write(json_str)