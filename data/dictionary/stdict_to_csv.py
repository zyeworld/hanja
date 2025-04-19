# 표준국어대사전 사전 내려받기 이후 한자어 추출

import pandas as pd

dfs = []
file_names = list(map(str, range(30000, 420001, 30000))) + ['436134']

for name in file_names:
    df = pd.read_excel(f'data_temp/1435015_{name}.xls')

    # Filter: 단어, 한자어/혼종어, 품사 존재, 용례 존재
    df_hanjaeo = df[(df['구성 단위'] == '단어') & ((df['고유어 여부'] == '한자어') | (df['고유어 여부'] == '혼종어')) & (df['품사'] != '「품사 없음」') & (df['용례'].notna())]
    df_hanjaeo = df_hanjaeo[df_hanjaeo['원어'].apply(lambda x: len(str(x))) > 1]

    df_hanjaeo = df_hanjaeo[['어휘', '원어', '원어·어종', '품사', '뜻풀이', '용례', '속담', '관용구']]

    print(df_hanjaeo.info())
    dfs.append(df_hanjaeo)

df_final = pd.concat(dfs, ignore_index=True)
print(df_final.info())
df_final.to_csv('data/dictionary/stdict.csv', index=False)