import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_movie_details(movie_id):
    api_key = "b4af919b50b76eee5974d1c06e5dbbde"
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_url = "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
    movie_url = f'https://www.themoviedb.org/movie/{movie_id}'  # TMDB movie page link
    return poster_url, movie_url

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_url = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster, url = fetch_movie_details(movie_id)
        recommended_movies_poster.append(poster)
        recommended_movies_url.append(url)
    
    return recommended_movies, recommended_movies_poster, recommended_movies_url

# Load Movie Data
movies_list = pickle.load(open('Movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 **Movie Recommender System**")
st.markdown("Get personalized movie recommendations based on your favorite movie! 🍿")

selected_movie_name = st.selectbox("🔍 **Search for a Movie:**", movies['title'].values)

if st.button("💡 **Recommend**"):
    st.markdown("You may also like:")
    names, posters, urls = recommend(selected_movie_name)
    
    cols = st.columns(6)
    for col, name, poster, url in zip(cols, names, posters, urls):
        with col:
            st.markdown(
                f'<a href="{url}" target="_blank">'
                f'<img src="{poster}" style="width:100%; border-radius:15px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);"/>'
                f'<p style="text-align:center;">{name}</p>'
                f'</a>',
                unsafe_allow_html=True
            )

st.markdown("---")
st.markdown("💻 Developed by Abhinav Aras & Shripad Joshi ❤️ using [Streamlit](https://streamlit.io/) and TMDB API.")
