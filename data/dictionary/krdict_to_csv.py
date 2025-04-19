# 한국어기초사전 사전 내려받기 이후 한자어 추출

import pandas as pd

dfs = []
file_names = ['30969', '31413']

for name in file_names:
    df = pd.read_excel(f'data_temp/1213850_{name}.xls')

    print(df.info())
    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)
print(df_final.info())
df_final.to_csv('data/dictionary/krdict.csv', index=False)