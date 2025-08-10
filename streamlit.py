import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Download similarity.pkl from Google Drive if not already present
url = 'https://drive.google.com/file/d/1dAkM4GRJRn8fhJTv1xoLMHEaap_zO8tg/view?usp=drive_link'
output = 'similarity.pkl'
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Load other local pickle file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[2:7]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies

st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for rec in recommendations:
        st.write(rec)

