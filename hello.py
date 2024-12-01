# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 加载数据
@st.cache
def load_data():
    # 使用GitHub上的CSV文件链接或本地文件路径
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/d6d8457d63867b435bfdea9c541afd71495829f9/movies_dataset.csv"
    return pd.read_csv(url, encoding='ISO-8859-1')

df = load_data()

# 页面设置：添加页面标题和图标
st.set_page_config(page_title="Movie Data Dashboard", page_icon="🎬", layout="wide")

# 页面标题
st.title("🎬 Movie Data Dashboard")

# 引导信息，使用Markdown来渲染文本
st.markdown("""
    **Welcome to the Movie Data Dashboard!** 🎥  
    This app allows you to explore a variety of insights from a vast movie dataset.  
    Whether you're interested in genre distributions, director search, or discovering hidden gems, this dashboard has it all.

    ### 🔥 Features:
    1. **Overview**: A guide to the app and its features.
    2. **Genre Distribution**: View the most popular genres.
    3. **Top Genres by Country**: Discover the top genres by country.
    4. **Search by Director**: Search movies by your favorite directors.
    5. **Search by Movie**: Find your favorite movies and get detailed information.
    6. **Hidden Gems**: Explore high-rated movies with low votes.
    
    Ready to explore? Start by selecting an option from the sidebar! 🌟
""")

# 功能选择，使用 `selectbox` 或 `radio` 使用户有操作感
option = st.sidebar.radio(
    "Choose a feature:",
    ("Overview", "Genre Distribution", "Top Genres by Country", "Search by Director", "Search by Movie", "Hidden Gems")
)

# 功能 1: 数据概览
if option == "Overview":
    st.header("Overview")
    
    st.write("""
    Welcome to the **Movie Data Dashboard**! This app allows you to explore various trends and insights from a large movie dataset. Here's a quick guide to the features available in this dashboard:

    ### 1. **Overview**
    - This section introduces the app and gives you a quick overview of what you can explore in the different sections of the app.

    ### 2. **Genre Distribution**
    - Explore the distribution of movie genres across the dataset. View how different genres are represented and analyze the most common genres.

    ### 3. **Top Genres by Country**
    - Dive into the most popular genres across different countries. Select a country and view the top 10 genres that are most watched in that country.

    ### 4. **Search by Director**
    - Search for movies directed by a specific director. You can view all movies by the selected director and their average IMDB rating.

    ### 5. **Search by Movie**
    - If you have a movie title in mind, use this feature to search for it. You'll see the movie's details, including its genre, rating, and other related information.

    ### 6. **Hidden Gems**
    - Looking for some underrated movies? This section highlights high-rated movies with fewer votes, perfect for discovering hidden gems in your favorite genres!

    Feel free to explore each feature and discover new insights from the dataset.
    """)
    
    # 你可以使用 `st.button()` 来增加交互元素，让用户点击后加载不同的内容
    if st.button("Let's Explore!"):
        st.write("Let's dive into the **Genre Distribution** section!")

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

# 功能 1: 按导演搜索
st.header("Search by Director")
director_name = st.text_input("Enter Director's Name:")
if director_name:
    matching_directors = sorted(
        [director for director in df['director'].dropna().unique() 
         if director_name.lower() in director.lower()]
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
