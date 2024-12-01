import streamlit as st
import pickle
import requests
import os
import gdown

# Function to download similarity.pkl from Google Drive
def download_similarity_file():
    # Correct Google Drive URL for direct download
    url = "https://drive.google.com/uc?id=1ki3ZByfEKMESN9z9UJIE8ZPl1_a02SnX&export=download"  # Corrected link
    output_path = "similarity.pkl"  # Path to save the file locally

    try:
        gdown.download(url, output_path, quiet=False)
        st.write("Downloaded similarity.pkl successfully!")
    except Exception as e:
        st.error(f"Failed to download similarity.pkl. Error: {str(e)}")
        st.stop()

# Check if similarity.pkl exists, if not, download it
if not os.path.exists("similarity.pkl"):
    st.write("Downloading similarity.pkl...")
    download_similarity_file()

# Load the movie list and similarity file after download
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))  # This line loads the .pkl file

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=97d5a607fcee6660300b0aa8ea11b164&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id

        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies_list['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Create columns explicitly using st.columns
    col1, col2, col3, col4, col5 = st.columns(5)

    if len(names) > 0:
        with col1:
            st.header(names[0])
            st.image(posters[0])

    if len(names) > 1:
        with col2:
            st.header(names[1])
            st.image(posters[1])

    if len(names) > 2:
        with col3:
            st.header(names[2])
            st.image(posters[2])

    if len(names) > 3:
        with col4:
            st.header(names[3])
            st.image(posters[3])

    if len(names) > 4:
        with col5:
            st.header(names[4])
            st.image(posters[4])
