import streamlit as st
import pandas as pd
import plotly.express as px
import base64

def download_csv(data, file_name):
    # ダウンロードボタンを表示
    # CSV ファイルとしてデータフレームをダウンロード
    csv = data.to_csv(index=False, encoding='utf-8-sig')  # UTF-8 BOM 形式で保存
    b64 = base64.b64encode(csv.encode()).decode()  # CSV を base64 エンコード
    filename = st.text_input("保存時のファイル名を入力してください", "{}.csv".format(file_name))  # ユーザーにファイル名を入力してもらう
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

    return None

# タイトル。最もサイズが大きい。ページタイトル向け
st.title('相関分析と高相関の指標をPLOT')

upload_file = st.file_uploader("データをアップロードしてください")

if upload_file is not None:

    
    data = pd.read_csv(
        upload_file,
        engine='python'
        )
    
    data_cor = data.drop(columns="ds")

    st.header("目的変数選択")
    y = st.selectbox("目的変数を選択してください", data_cor.columns)

    data_cor = data_cor.corr()[y]
    data_cor = data_cor.sort_values(ascending=False)
    data_cor = data_cor[data_cor.index != y]
    data_cor = data_cor.sort_values(ascending=False)

    st.header("目的変数に対する相関ランキング")
    download_csv(data_cor, y)
    st.write(data_cor)

    # 相関上位2つだけPLOT
    data_cor_top_3 = data_cor.head(2).index.tolist()
    data_cor_top3_for_plot = data[["ds", y] + data_cor_top_3]

    # グラフの描画
    fig = px.line(data_cor_top3_for_plot, x='ds', y=[y] + data_cor_top_3, title='目的変数と相関上位2変数のPLOT')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    # プロットをStreamlitで表示
    st.plotly_chart(fig)


    st.header("推移の確認")
    col_names = data.drop(columns="ds").columns

    usecols = st.multiselect(
            '比較したいカラムを2つ入れてください',
            list(col_names),
            [])

    # グラフの描画
    fig = px.line(data, x='ds', y=usecols, title='時系列PLOT')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    # プロットをStreamlitで表示
    st.plotly_chart(fig)


    

