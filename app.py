import streamlit as st
import pickle
import pandas as pd
import requests

st.markdown(
    """
    <style>
    /* Image hover effect */
    .movie-poster {
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        border-radius: 15px;
    }
    .movie-poster:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def fetch_poster(movie_id):
    response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b4af919b50b76eee5974d1c06e5dbbde'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[0:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_list = pickle.load(open('Movies.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title("🎬 **Movie Recommender System**")
st.markdown("Get personalized movie recommendations based on your favorite movie! 🍿")
selected_movie_name = st.selectbox("🔍 **Search for a Movie:**", movies['title'].values)

if st.button("💡 **Recommend**"):
    st.markdown("You may also like:")
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(
                    f'<div class="movie-poster" style="text-align:center; width: 100%;">'
                    f'<img src="{posters[0]}" alt="{names[0]}" style="width: 80%; border-radius: 15px;">'
                    f'<p>{names[0]}</p></div>',
                    unsafe_allow_html=True,
                )
    with col2:
        st.markdown(
                    f'<div class="movie-poster" style="text-align:center; width: 100%;">'
                    f'<img src="{posters[1]}" alt="{names[1]}" style="width: 80%; border-radius: 15px;">'
                    f'<p>{names[1]}</p></div>',
                    unsafe_allow_html=True,
                )
    with col3:
        st.markdown(
                    f'<div class="movie-poster" style="text-align:center; width: 100%;">'
                    f'<img src="{posters[2]}" alt="{names[2]}" style="width: 80%; border-radius: 15px;">'
                    f'<p>{names[2]}</p></div>',
                    unsafe_allow_html=True,
                )  
    with col4:
        st.markdown(
                    f'<div class="movie-poster" style="text-align:center; width: 100%;">'
                    f'<img src="{posters[3]}" alt="{names[3]}" style="width: 80%; border-radius: 15px;">'
                    f'<p>{names[3]}</p></div>',
                    unsafe_allow_html=True,
                )
    with col5:
        st.markdown(
                    f'<div class="movie-poster" style="text-align:center; width: 100%;">'
                    f'<img src="{posters[4]}" alt="{names[4]}" style="width: 80%; border-radius: 15px;">'
                    f'<p>{names[4]}</p></div>',
                    unsafe_allow_html=True,
                )   
    with col6:
        st.markdown(
                    f'<div class="movie-poster" style="text-align:center; width: 100%;">'
                    f'<img src="{posters[5]}" alt="{names[5]}" style="width: 80%; border-radius: 15px;">'
                    f'<p>{names[5]}</p></div>',
                    unsafe_allow_html=True,
                )    

st.markdown("---")
st.markdown("💻 Developed by Abhinav Aras & Shripad Joshi ❤️ using [Streamlit](https://streamlit.io/) and The Movie Database (TMDB) API.")            