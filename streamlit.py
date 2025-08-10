import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Configuration
SIMILARITY_FILE_ID = '1dAkM4GRJRn8fhJTv1xoLMHEaap_zO8tg'  # Replace with actual ID
MOVIE_DICT_FILE_ID = '1E86_gfrucNdMiQMvsDEpLWo1kx8OYDhj'  # Replace with actual ID

@st.cache_resource
def load_data():
    try:
        # Download similarity.pkl if not exists
        if not os.path.exists('similarity.pkl'):
            sim_url = f'https://drive.google.com/uc?id={SIMILARITY_FILE_ID}'
            gdown.download(sim_url, 'similarity.pkl', quiet=False)
        
        # Download movie_dict.pkl if not exists
        if not os.path.exists('movie_dict.pkl'):
            dict_url = f'https://drive.google.com/uc?id={MOVIE_DICT_FILE_ID}'
            gdown.download(dict_url, 'movie_dict.pkl', quiet=False)
        
        # Load data
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
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Get top 5 similar movies
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
