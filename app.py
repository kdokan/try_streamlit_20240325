import streamlit as st
import pandas as pd
import plotly.express as px

# タイトル。最もサイズが大きい。ページタイトル向け
st.title('相関分析と高相関の指標をPLOT')



upload_file = st.file_uploader("データをアップロードしてください")

if upload_file is not None:

    
    data = pd.read_csv(
        upload_file,
        engine='python'
        )
    
    data_cor = data.drop(columns="ds")
    data_cor = data_cor.corr()
    data_cor = data_cor[data_cor['バファリン_Google検索数'] != 'バファリン_Google検索数']
    data_cor = data_cor["バファリン_Google検索数"]
    data_cor = data_cor.sort_values(ascending=False)

    st.header("相関ランキング")
    st.write(data_cor)

#st.markdown('### アクセスログ（先頭5件）')
#st.write(data.head(5))

    st.header("推移の比較")
    #data = pd.read_csv('data/input.csv')
    col_names = data.drop(columns="ds").columns

    #usecol = st.radio(
    #        'plotする変数',
    #       col_names)

    # 時系列データを線グラフとしてプロット
    #fig = px.line(data, x='ds', y=usecol, title='時系列PLOT')

    # プロットをStreamlitで表示
    #st.plotly_chart(fig)


    #st.header("推移の比較")


    usecols = st.multiselect(
            '比較したいカラムを2つ入れてください',
            list(col_names),
            [])

    # グラフの描画
    fig = px.line(data, x='ds', y=usecols, title='時系列PLOT')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    # プロットをStreamlitで表示
    st.plotly_chart(fig)


    

