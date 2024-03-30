

#%%

import pandas as pd
import numpy as np

# サンプルデータの数
num_samples = 2000

# idを生成
ids = range(1, num_samples + 1)

# demo_ageをランダムに生成 (例: 18歳から70歳の間でランダムに生成)
sex = np.random.randint(0, 2, size=num_samples)
age = np.random.randint(18, 71, size=num_samples)

# weightをランダムに生成 (例: 40kgから100kgの間でランダムに生成)
weight = np.random.randint(3, 10, size=num_samples)

# media_youtubeをランダムに生成 (例: 0から100までのランダムな数値)
media_youtube = np.random.randint(0, 101, size=num_samples)

# media_facebook_instagramをランダムに生成 (例: 0から100までのランダムな数値)
media_facebook_instagram = np.random.randint(0, 101, size=num_samples)

# データフレームを作成
data = {
    'id': ids,
    'sex': sex,
    'age': age,
    'weight': weight,
    'media_youtube': media_youtube,
    'media_facebook_instagram': media_facebook_instagram
}

data = pd.DataFrame(data)

# 性別情報付与
data['sex'] = data['sex'].replace({0: '女性', 1: '男性'})
# 年齢情報付与
# 年代を判定する関数
def determine_age_group(age):
    if 10 <= age < 30:
        return "10-20代"
    elif 30 <= age < 40:
        return "30代"
    elif 40 <= age < 50:
        return "40代"
    elif 50 <= age < 60:
        return "50代"
    elif 60 <= age < 70:
        return "60代"
    else:
        return None
data["age"] = data["age"].apply(determine_age_group)

# 性年代結合
# sexとageを結合するカスタム関数
def unite_sex_age(row):
    return f"{row['sex']}{row['age']}"
data['sex_age'] = data.apply(unite_sex_age, axis=1)

data = data[["id","sex","age","weight","media_youtube","media_facebook_instagram"]]

# データフレームを表示
print(data)
data.to_csv('../data/sample_data.csv', index=False)  

# %%
