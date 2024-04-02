import pickle
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get(path: str):
    with open(path, "r") as p:
        return json.load(p)

def movie_section():
    st.header('🎥Movie Recommender System🍿')

    path = get("./mov.json")
    st_lottie(path)

    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])

    local_css("./style.css")

    animation_symbol = "❄️"

    st.markdown(
        f"""
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        <div class ="snowflake">{animation_symbol}</div>
        """,
        unsafe_allow_html=True
    )

def song_section():
    st.header('Song Recommender System')

    lottie_path = get("./img.json")

    # Wrap both the Lottie animation and the GIF within a single div and align it to the center using CSS
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <div>
                {st_lottie(lottie_path, width=400, height=400)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # Style the text to align to the middle, increase the size, and change the color to blue
    st.markdown("""
                <p style='text-align:center; font-size: 40px; color: yellow;'>
                    Sorry for the inconvenience, We are currently working on this
                </p>
                """, 
                unsafe_allow_html=True)

choice = st.sidebar.radio(
    label='Choose from the options',
    options=["Movie recommender", "Song recommender"],
)

if choice == "Movie recommender":
    movie_section()

if choice == "Song recommender":
    song_section()
