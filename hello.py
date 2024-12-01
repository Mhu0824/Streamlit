# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 加载数据
@st.cache_data
def load_data():
    try:
        # 替换为你的 CSV 文件路径
        df = pd.read_csv("movies_dataset.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# 数据加载
df = load_data()

# 设置页面布局
st.set_page_config(layout="wide")
st.title("🎬 Movie Explorer Dashboard")

# 功能 1: 按导演搜索
st.header("Search by Director")
director_name = st.text_input("Enter Director's Name:")
if director_name:
    matching_directors = sorted(
        set(df['director'].dropna().unique())  # 提取所有导演名字
        if director_name.lower() in director.lower()
    )
    selected_director = st.selectbox("Select a Director:", matching_directors)
    if selected_director:
        director_movies = df[df['director'] == selected_director]
        st.write(f"Movies by {selected_director}:")
        st.dataframe(
            director_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes']].rename(
                columns={
                    'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                    'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes'
                }
            )
        )
        avg_rating = director_movies['imdbRating'].mean()
        st.write(f"Average IMDB Rating for {selected_director}'s movies: {avg_rating:.2f}")

# 功能 2: 按电影搜索
st.header("Search by Movie")
movie_name = st.text_input("Enter Movie Title:")
if movie_name:
    matching_movies = sorted(
        {f"{title.strip()} ({year})" for title, year in zip(df['title'], df['year']) 
         if pd.notna(title) and movie_name.lower() in title.lower()}
    )
    selected_movie_with_year = st.selectbox("Select a Movie:", matching_movies)
    if selected_movie_with_year:
        selected_movie, selected_year = selected_movie_with_year.rsplit(" (", 1)
        selected_year = selected_year.rstrip(")")
        movie_details = df[(df['title'] == selected_movie) & (df['year'] == int(selected_year))]
        if not movie_details.empty:
            director_name = movie_details['director'].iloc[0] if not movie_details.empty else "Unknown"
            st.write(f"Details for '{selected_movie} ({selected_year})' created by {director_name}:")
            st.dataframe(
                movie_details[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                    columns={
                        'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                        'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes', 
                        'rating': 'Rating', 'awards': 'Awards'
                    }
                )
            )

# 功能 3: 冷门佳作
st.header("Hidden Gems: High Ratings but Low Votes")
genre = st.selectbox("Select Genre:", sorted(df['genre_1'].dropna().unique()))
if genre:
    hidden_gems = df[(df['genre_1'] == genre) & (df['imdbVotes'] < 1000) & (df['imdbRating'] >= 8.0)]
    hidden_gems_sorted = hidden_gems.sort_values(by='imdbRating', ascending=False)
    if not hidden_gems_sorted.empty:
        st.write(f"Hidden Gems in {genre}:")
        st.dataframe(
            hidden_gems_sorted[['title', 'year', 'imdbRating', 'imdbVotes']].rename(
                columns={
                    'title': 'Title', 'year': 'Year', 
                    'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes'
                }
            )
        )
    else:
        st.write(f"No hidden gems found for {genre}.")
