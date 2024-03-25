#%%
# デモデータ作成
import pandas as pd


def clening_google_trend(path_data):
    # データ読み込み
    data = pd.read_csv(
        path_data
        , skiprows=1)

    # カラム名設定
    data = data.rename(
        columns = {
            "週":"ds"
        }
    )

    ## カラム名を正規表現で置換
    data.columns = data.columns.str.replace(r": (日本)", r"_Google検索数")

    # 日付型に変換
    data["ds"] = pd.to_datetime(data["ds"])

    return data



data_buffelin = clening_google_trend("data/buffelin.csv")
data_loxonin = clening_google_trend("data/loxonin.csv")
data_inbound = clening_google_trend("data/inbound.csv")
data_covid = clening_google_trend("data/covid.csv")
data_influenza = clening_google_trend("data/influenza.csv")

data = pd.merge(data_buffelin, data_loxonin, on = "ds", how="left")
data = pd.merge(data, data_inbound, on = "ds", how="left")
data = pd.merge(data, data_covid, on = "ds", how="left")
data = pd.merge(data, data_influenza, on = "ds", how="left")
data = data[data["ds"] >= "2020-01-19"]
data.to_csv('data/input.csv', index=False)  

# %%
data = pd.read_csv('data/input.csv')
data_cor = data.drop(columns="ds")
data_cor = data_cor.corr()
data_cor = data_cor["バファリン_Google検索数"]
data_cor = data_cor.sort_values(ascending=False)
# %%
