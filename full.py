import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# 加载数据
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/d6d8457d63867b435bfdea9c541afd71495829f9/movies_dataset.csv"
    data = pd.read_csv(url, encoding='ISO-8859-1')
    data['year'] = data['year'].astype(str).str.replace(r'\D', '', regex=True)
    data['title_clean'] = data['title'].str.strip().str.lower()
    data['year_clean'] = data['year'].str.strip()
    data['genre_1'] = data['genre_1'].str.strip()
    return data

df = load_data()

# 标题
st.title("🎬 Movie Data Dashboard")

# 功能选择
option = st.sidebar.radio(
    "Choose a feature:",
    (
        "Overview", 
        "Genre Distribution", 
        "Top Genres by Country", 
        "Search by Director", 
        "Search by Movie", 
        "Unearth Hidden Movies: Rate & Vote",
        "Compare Movie Rating to Genre Average"
    )
)

# 公共函数：绘制条形图
def plot_bar(data, x_col, y_col, title, x_label="", y_label=""):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=x_col, y=y_col, data=data, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    st.pyplot(fig)

# 功能 1: 数据概览
if option == "Overview":
    st.header("Overview")
    st.write("""
        Welcome to the Movie Data Explorer! This dashboard allows you to explore various aspects of a large movie dataset.
    """)

# 功能 2: 电影类型分布
elif option == "Genre Distribution":
    st.header("Genre Distribution")
    genres = pd.concat([df['genre_1'], df['genre_2'], df['genre_3'], df['genre_4'], df['genre_5']]).dropna()
    genre_counts = genres.value_counts()
    top_15_genres = genre_counts.head(15)
    other_count = genre_counts[15:].sum()
    top_15_genres_with_other = pd.concat([top_15_genres, pd.Series({"Other": other_count})])
    st.write("Top 15 Genres and 'Other':")
    st.write(top_15_genres_with_other)
    plot_bar(top_15_genres_with_other.reset_index(), x_col=0, y_col=1, title="Top 15 Genres and 'Other'")

# 功能 3: 不同国家电影类型
elif option == "Top Genres by Country":
    df['country'] = df['country'].str.split(", ")
    df_exploded = df.explode('country')[['country', 'genre_1']].dropna()
    country_genre_counts = df_exploded.groupby(['country', 'genre_1']).size().reset_index(name='count')
    countries = country_genre_counts['country'].unique()
    selected_country = st.selectbox("Select a Country:", sorted(countries))
    if selected_country:
        top_genres = country_genre_counts[country_genre_counts['country'] == selected_country].nlargest(10, 'count')
        st.write(f"Top Genres in {selected_country}:")
        st.write(top_genres)
        plot_bar(top_genres, x_col='count', y_col='genre_1', title=f"Top Genres in {selected_country}")

# 功能 4: 按导演名字搜索
elif option == "Search by Director":
    director_name = st.text_input("Enter Director's Name:")
    if director_name:
        matching_directors = sorted(
            {name.strip() for name in df['director'].dropna() if director_name.lower() in name.lower()}
        )
        selected_director = st.selectbox("Select a Director:", matching_directors)
        if selected_director:
            director_movies = df[df['director'].str.contains(selected_director, na=False)]
            st.write(f"Movies directed by {selected_director}:")
            st.dataframe(director_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes']])
            avg_rating = director_movies['imdbRating'].mean()
            st.write(f"Average IMDB Rating for {selected_director}'s movies: {avg_rating:.2f}")

# 功能 5: 按电影名字搜索
elif option == "Search by Movie":
    movie_name = st.text_input("Enter Movie Title:")
    if movie_name:
        matching_movies = sorted(
            {f"{title} ({year})" for title, year in zip(df['title_clean'], df['year_clean']) 
             if pd.notna(title) and movie_name.lower() in title}
        )
        selected_movie = st.selectbox("Select a Movie:", matching_movies)
        if selected_movie:
            title, year = selected_movie.rsplit(" (", 1)
            movie_details = df[(df['title_clean'] == title.lower()) & (df['year_clean'] == year.rstrip(")") )]
            st.dataframe(movie_details[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes']])

# 功能 6: 冷门佳作
elif option == "Unearth Hidden Movies: Rate & Vote":
    genre = st.selectbox("Select a Genre:", ["All"] + sorted(df['genre_1'].dropna().unique()))
    min_votes = st.number_input("Minimum Votes", value=0)
    max_votes = st.number_input("Maximum Votes", value=1000)
    rating_filter = st.slider("Select Rating Range", 0.0, 10.0, (7.0, 10.0))
    filtered_movies = df[
        ((df['genre_1'] == genre) | (genre == "All")) & 
        (df['imdbVotes'].between(min_votes, max_votes)) & 
        (df['imdbRating'].between(*rating_filter))
    ]
    st.dataframe(filtered_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes']])
