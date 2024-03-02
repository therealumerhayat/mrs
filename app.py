import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2d2c0e2656a714dfc4bd391b4e53a9a8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies  = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender")

selected_movie_name = st.selectbox(
'How would you like to be contacted?',
movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    num_cols = 5  # Number of columns you want
    col_layout = st.columns(num_cols)

    # Check if both lists have at least five elements
    if len(names) >= num_cols and len(posters) >= num_cols:
        for i in range(num_cols):
            with col_layout[i]:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.error("Both 'names' and 'posters' lists must have at least five elements.")
















