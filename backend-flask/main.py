import pandas as pd
import joblib
import json
from ast import literal_eval

loaded_knn_model, loaded_final_features = joblib.load('knn_model.joblib')
df = pd.read_csv('anime.csv')
data = df[['id','title','start_date','end_date','synopsis','num_episodes','studios','genres','main_picture_medium','main_picture_large','popularity']]
date_format = "%Y-%m-%d %H:%M:%S"
data.loc[:,'genres'] = data['genres'].apply(literal_eval)
data.loc[:,'studios'] = data['studios'].apply(literal_eval)
df['title'] = df['title'].apply(lambda x: x.lower())

# Function to get top-k similar anime titles using KNN
def get_top_similar_anime_knn(title, k):
    # Get the index of the anime with the given title
    title = title.lower()
    if title not in df['title'].values:
        print("Error: The target anime title is not in the dataset.")
        return []

    anime_index = df[df['title'] == title].index[0]

    # Get the indices and distances of the k most similar anime (including itself)
    distances, indices = loaded_knn_model.kneighbors(loaded_final_features[anime_index].reshape(1, -1), n_neighbors=k)

    # Get the top k similar anime (including the target anime itself)
    top_k_indices = indices.flatten()
    top_k_anime = df.iloc[top_k_indices]['id'].tolist()[1:]
    return top_k_anime

def get_recommendations(target_anime_title):
    recommended_anime_id = get_top_similar_anime_knn(target_anime_title, k=11)
    rows_by_indices = data[data['id'].isin(recommended_anime_id)]
    results = rows_by_indices.to_json(orient='records')
    return json.loads(results)

def get_popular_anime():
    popular_anime = data.sort_values(by=['popularity'])[:10]
    results = popular_anime.to_json(orient='records')
    return json.loads(results)

def get_anime_from_anime_id(anime_id):
    if anime_id not in data['id'].values:
        return {}
    anime = data[data['id']==anime_id]
    result = anime.to_json(orient='records')
    search = json.loads(result)[0]
    return search
