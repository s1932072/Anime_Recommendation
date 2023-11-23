#This is Frontend written by streamlit
import streamlit as st
import pandas as pd
import json
import requests

st.title("アニメ推薦システム")
st.header("アニメを推薦します")

# ジャンルを選ぶスペースを横に配置
col1, col2 = st.columns(2)
genre = pd.read_json("genres.json")
with col1:
    selected_genre = st.selectbox("見たいアニメのジャンルを選択してください",genre)
    #ここで選んだジャンルをバックエンドに送信する

    # FastAPIのエンドポイントにPOSTリクエストを送信
    response = requests.post("http://localhost:8000/select_genre", json ={"selected_genre": selected_genre})    


with col2:
    if response.status_code == 200:
        anime_names = response.json()["selected_japanese_names"]
        selected_anime = st.selectbox("以下からアニメを選択してください", anime_names)
    else:
        st.write("エラーが発生しました。")




    if st.button("おすすめを表示"):
    # FastAPIのエンドポイントにPOSTリクエストを送信
        response = requests.post("http://localhost:8000/recommend_anime", json ={"selected_anime_title": selected_anime})
    if response.status_code == 200:
        recommended_animes = response.json().get("recommended_animes", [])  
        if recommended_animes:
            st.write(anime_names + "が好きなあなたにおすすめなアニメは以下の通りです。")
            for i, anime in enumerate(recommended_animes):
                st.write(f"{i+1}: {anime}")
        else:
            st.write("『おすすめを表示』を押してください")
    else:
        st.write("エラーが発生しました。")
