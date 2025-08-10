import streamlit as st
import pickle
import pandas as pd
import requests
import os

SIMILARITY_FILE_ID = '1fYHwVrnPHGsJ3r_k-zx6c9Wdv0__tW6_'  
MOVIE_DICT_FILE_ID = '1nsWnBymSJPbwCiEGU2TgSba8sfl8KBs4'  

def download_from_gdrive(file_id, dest_path):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    with open(dest_path, 'wb') as f:
        f.write(response.content)

@st.cache_resource
def load_data():
    try:
        if not os.path.exists('similarity.pkl'):
            download_from_gdrive(SIMILARITY_FILE_ID, 'similarity.pkl')
        
        if not os.path.exists('movie_dict.pkl'):
            download_from_gdrive(MOVIE_DICT_FILE_ID, 'movie_dict.pkl')
        
        movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

movies, similarity = load_data()

if movies is None or similarity is None:
    st.stop()

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        return [movies.iloc[i[0]].title for i in movies_list]
    except IndexError:
        st.error("Movie not found in database")
        return []
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    if recommendations:
        st.subheader("Recommended Movies:")
        for rec in recommendations:
            st.write(rec)
