import streamlit as st

# タイトル。最もサイズが大きい。ページタイトル向け
st.title('aaaa')

# ヘッダ。２番目に大きい。項目名向け
st.header('Header')

# サブレベルヘッダ。３番目に大きい。小項目向け
st.subheader('Sub Header')

# 普通のテキスト。Html や Markdown のパースはしない。
st.text('Text')

# 普通のテキストその２。Markdown のパースをする他、複数の値を渡せる。
st.write('### Current date: ', date.today())