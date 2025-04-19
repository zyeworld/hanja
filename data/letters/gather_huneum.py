import json

letter_filenames = [f'data/letters/letter_{x}.json' for x in ['8', '7p', '7', '6p', '6', '5p', '5', '4p', '4', '3p', '3', '2', '1', '0p', '0']]
dump_filename = 'data/letters/huneum.json'

huneum_data = {} # {'가': ['집', '노래', ...]}

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
                    huneum_data[eum] = [hun]
                elif hun not in huneum_data[eum]:
                    huneum_data[eum].append(hun)

for key in huneum_data:
    huneum_data[key].sort()

json_str = json.dumps(huneum_data, ensure_ascii=False, indent=0, separators=(',', ':'), sort_keys=True)
with open(dump_filename, 'w') as file:
    file.write(json_str)