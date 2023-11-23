from fastapi import FastAPI 
import pandas as pd
from pydantic import BaseModel
from scipy.sparse import  load_npz
import pickle
app = FastAPI()


#各種データの読み込み
anime = pd.read_csv("merged_anime.csv")
anime_pivot_reversed_sparse = load_npz('anime_pivot_reversed_sparse.npz')

with open('knn_model.pkl', 'rb') as file:
    model_knn = pickle.load(file)


#フロントで選択されたジャンルを受け取り、そのジャンルに該当するアニメの日本語名を返す
class Genre(BaseModel):
    selected_genre: str

@app.post("/select_genre")
def select_genre(genre: Genre):
    select_rows = anime[anime["Genres_x"].str.contains(genre.selected_genre, case=False)]
    japanese_names = select_rows["Japanese name"].values.tolist()
    return {"selected_japanese_names": japanese_names}


#選択されたアニメの日本語名からIDを取得し、そのIDをもとに類似度の高いアニメを返す
class AnimeTitle(BaseModel):
    selected_anime_title: str

@app.post("/recommend_anime")
def selected_anime(selected_anime: AnimeTitle):
    # 選択されたアニメの日本語名からIDを取得
    selected_row = anime[anime["Japanese name"] == selected_anime.selected_anime_title]

    MAL_ID = selected_row["MAL_ID"].values[0]

    #KNNで類似度の高いアニメを取得
    n_neighbors = 10
    distances, indices = model_knn.kneighbors(anime_pivot_reversed_sparse[MAL_ID], n_neighbors=n_neighbors+1)
    
    # 推薦されたアニメIDのリスト
    recommended_anime_ids = [anime.index[indices.flatten()[i]] for i in range(1, len(distances.flatten()))]

    # データベース内に存在するアニメIDのリストを取得　（MAL_IDは存在しない数字があり、それを出力することがあるため実施）
    existing_anime_ids = anime['MAL_ID'].values

    # 推薦されたアニメIDをデータベース内に存在するものだけにフィルタリング
    valid_recommended_anime_ids = [anime_id for anime_id in recommended_anime_ids if anime_id in existing_anime_ids]

    # 推薦されたアニメ名のリストを作成
    recommended_anime_names = [anime[anime['MAL_ID'] == anime_id]['Japanese name'].values[0] for anime_id in valid_recommended_anime_ids]

    return {"recommended_animes": recommended_anime_names}

