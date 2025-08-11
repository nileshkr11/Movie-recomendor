import streamlit as st
import pickle
import pandas as pd
import requests 
import gdown

simillarity='1fYHwVrnPHGsJ3r_k-zx6c9Wdv0__tW6_'
moviedict='1nsWnBymSJPbwCiEGU2TgSba8sfl8KBs4'

prefix = 'https://drive.google.com/uc?/export=download&id='


gdown.download(prefix+simillarity)
gdown.download(prefix+moviedict)


movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
similarity=pickle.load(open('similarity.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def recommend (movie):
    movie_index = movies[movies['title'] == movie].index [0]
    distances = similarity[movie_index]
    movies_list = sorted (list (enumerate (distances)), reverse=True, key=lambda x:x[1])[2:7]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        # recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies

st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values)
if st.button('Recommend'):
    recomendations=recommend(selected_movie_name)
    for i in recomendations:
        st.write(i)

