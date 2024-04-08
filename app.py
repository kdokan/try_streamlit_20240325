#%%
import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
from statsmodels.tsa.seasonal import STL

# データの読み込み
raw_data = pd.read_csv("data/input.csv")
raw_data["ds"] = pd.to_datetime(raw_data["ds"])

# 目的変数のカラム名のリスト作成
y_columns = ["バファリン_Google検索数", "ロキソニン_Google検索数"]


# 説明変数のカラム名のリスト作成
X_columns = ["インバウンド_Google検索数", "コロナ_Google検索数", "インフルエンザ_Google検索数"]

# %%
# app
y = st.sidebar.selectbox("目的変数を選択してください", y_columns)
# ユーザーが選択したカラムの合計を計算
select_stl_factor_columns = st.sidebar.multiselect('目的変数の加味する要素を選択してください', ["トレンド","季節性","残差"], default=["トレンド", "季節性", "残差"])

X = st.sidebar.selectbox("比較する説明変数を選択してください", X_columns)

# 開始日と終了日の初期値を設定
start_date = datetime.date(2020, 1, 19)
end_date = datetime.date(2024, 3, 17)

# 開始日と終了日のスライダーを表示
selected_start_date, selected_end_date = st.sidebar.slider(
    '期間選択',
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format='YYYY-MM-DD'
)

selected_start_date = pd.to_datetime(selected_start_date)  # datetime64[ns]型に変換
selected_end_date = pd.to_datetime(selected_end_date) 

data = raw_data[(raw_data["ds"]>=selected_start_date) & (raw_data["ds"]<=selected_end_date)]


#####
# STL分解
#####
stl = STL(
    data[y]
    , period=52 # 今回習字データなので
    , robust=True)
stl_series = stl.fit()

# STL分解結果のデータ
data_stl = pd.DataFrame()
data_stl[y] = stl_series.observed #観測データ（STL分解前の元のデータ）＝トレンド＋季節性＋残差
data_stl["トレンド"] = stl_series.trend    #トレンド（trend）
data_stl["季節性"] = stl_series.seasonal #季節性（seasonal）
data_stl["残差"] = stl_series.resid    #残差（resid）
data_stl["ds"] = data["ds"]
if select_stl_factor_columns:
    data_stl["sum_select_factor"] = data_stl[select_stl_factor_columns].sum(axis=1)
else:
    data_stl["sum_select_factor"] = 0

# プロット用のデータを作成
plot_data = []
for column in select_stl_factor_columns:
    plot_data.append(go.Scatter(x=data_stl['ds'], y=data_stl[column], mode='lines', name=column))

# レイアウトの設定
layout = go.Layout(
    title='選択された要素のプロット',
    xaxis=dict(title='日付'),
    yaxis=dict(title='値')
)

# プロット
fig = go.Figure(data=plot_data, layout=layout)

# Streamlitでプロットを表示
st.plotly_chart(fig)



####
# 時系列プロットを描画
####
#st.subheader("時系列プロット")

# 時系列プロットを描画
fig = make_subplots(specs=[[{"secondary_y": True}]])  # 2つのy軸を持つプロットを作成

# 目的変数のプロット
fig.add_trace(go.Scatter(x=data["ds"], y=data_stl["sum_select_factor"], mode='lines', name=y), secondary_y=False)

# 説明変数のプロット
fig.add_trace(go.Scatter(x=data["ds"], y=data[X], mode='lines', name=X), secondary_y=True)

# y軸の範囲を0から最大値までに設定
y_max = max(data[y].max(), data[X].max())

# レイアウトの設定
fig.update_layout(
    title = "時系列plot",
    xaxis_title="ds",
    yaxis_title=y,
    yaxis2_title=X,
    yaxis=dict(range=[0, y_max]),  # y軸の範囲を0から最大値までに設定
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig)

# 散布図を描画
#st.subheader("散布図")
fig_scatter = px.scatter(x=data[X], y=data_stl["sum_select_factor"])
# アスペクト比を正方形に設定
fig_scatter.update_layout(
    title = "散布図",
    width=400,  # 幅を400pxに設定
    height=400,  # 高さを400pxに設定
    margin=dict(l=20, r=20, t=40, b=20),  # マージンを設定
    autosize=False,  # 自動サイズ調整を無効にする
    plot_bgcolor='rgba(0,0,0,0)',  # プロットの背景色を透明にする
    paper_bgcolor='rgba(0,0,0,0)',  # ページの背景色を透明にする
    xaxis=dict(zeroline=False, showgrid=False, range=[0, max(data[X])]),  # x軸の範囲を0からxmax_valueまでに設定
    yaxis=dict(zeroline=False, showgrid=False, range=[0, max(data[y])]),  # y軸の範囲を0からymax_valueまでに設定
)
st.plotly_chart(fig_scatter)
# %%


# %%
