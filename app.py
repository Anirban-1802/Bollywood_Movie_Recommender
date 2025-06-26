import streamlit as st
import pickle
import pandas as pd

# Load model.pkl which contains the dataframe and similarity matrix
model_data = pickle.load(open('model.pkl', 'rb'))
new_df = model_data['data']
similarity = model_data['similarity']

# ✅ Fallback poster image (online URL)
FALLBACK_POSTER = "https://png.pngtree.com/thumb_back/fh260/back_our/20190622/ourmid/pngtree-minimalist-film-festival-film-and-tv-movie-poster-image_220289.jpg"

# Get safe poster URL or fallback
def get_poster_url(poster):
    if isinstance(poster, str) and poster.startswith("http") and len(poster.strip()) > 0:
        return poster
    return FALLBACK_POSTER

# Recommendation function
def recommend(movie):
    movie_index = new_df[new_df['movie_name'] == movie].index[0]
    distances = list(enumerate(similarity[movie_index]))
    movies_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    posters = []
    years = []
    ratings = []

    for i in movies_list:
        movie_data = new_df.iloc[i[0]]
        recommended_movies.append(movie_data.movie_name)
        posters.append(get_poster_url(movie_data.poster_url))
        years.append(movie_data.year)
        ratings.append(movie_data.rating)

    return recommended_movies, posters, years, ratings

# ---------- Streamlit UI ----------
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie", new_df['movie_name'].values)

if st.button("Recommend"):
    names, posters, years, ratings = recommend(selected_movie)
    cols = st.columns(5)

    for idx in range(5):
        with cols[idx]:
            st.markdown(
                f"""
                <div style="height: 300px; overflow: hidden; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                    <img src="{posters[idx]}" style="max-height: 100%; object-fit: contain;" />
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"<div style='text-align: center; font-weight: bold; margin-top: 10px;'>{names[idx]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;'>📅 {years[idx]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;'>⭐ {ratings[idx]}</div>", unsafe_allow_html=True)
