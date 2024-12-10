import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/d6d8457d63867b435bfdea9c541afd71495829f9/movies_dataset.csv"
    return pd.read_csv(url, encoding='ISO-8859-1')

df = load_data()

# 清理数据函数
def clean_data(data):
    data['year'] = data['year'].astype(str).str.replace(r'\D', '', regex=True)
    data['title_clean'] = data['title'].str.strip().str.lower()
    data['year_clean'] = data['year'].astype(str).str.strip()
    return data

df = clean_data(df)

# 通用绘图函数
def plot_bar(data, x_col, y_col, title, x_label=None, y_label=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=x_col, y=y_col, data=data, ax=ax)
    ax.set_title(title)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    st.pyplot(fig)

# 通用表格展示函数
def display_table(data, columns_mapping, title=None):
    table = data.rename(columns=columns_mapping)
    if title:
        st.write(title)
    st.dataframe(table)

# 标题
st.title("🎬 Movie Data Dashboard")

# 功能选择
option = st.sidebar.radio(
    "Choose a feature:",
    ("Overview", "Genre Distribution", "Top Genres by Country", "Search by Director", "Search by Movie", "Unearth Hidden Movies: Rate & Vote")
)

# 功能 1: 数据概览
if option == "Overview":
    st.header("Overview")
    st.write("""
        Welcome to the Movie Data Explorer! This dashboard allows you to explore various aspects of a large movie dataset, 
        including insights into movie genres, ratings, countries, directors, and more.
    """)

# 功能 2: 电影类型分布
elif option == "Genre Distribution":
    st.header("Genre Distribution")
    genres = pd.concat([
        df['genre_1'].str.strip(),
        df['genre_2'].str.strip(),
        df['genre_3'].str.strip(),
        df['genre_4'].str.strip(),
        df['genre_5'].str.strip()
    ]).dropna()
    genre_counts = genres.value_counts()
    st.write("All Genres and Their Counts:")
    st.write(genre_counts)
    top_15_genres = genre_counts.head(15)
    other_count = genre_counts[15:].sum()
    top_15_genres_with_other = pd.concat(
        [top_15_genres, pd.Series({"Other": other_count})]
    ).reset_index()
    top_15_genres_with_other.columns = ['Genre', 'Count']
    plot_bar(top_15_genres_with_other, 'Count', 'Genre', "Top 15 Genres and 'Other'")

# 功能 3: 不同国家电影类型
elif option == "Top Genres by Country":
    df['country'] = df['country'].str.split(", ")
    df_exploded = df.explode('country')
    df_exploded = df_exploded[['country', 'genre_1']].dropna()
    df_exploded['genre_1'] = df_exploded['genre_1'].str.strip()
    country_genre_counts = df_exploded.groupby(['country', 'genre_1']).size().reset_index(name='count')
    countries = country_genre_counts['country'].unique()
    selected_country = st.selectbox("Select a Country:", sorted(countries))
    if selected_country:
        top_genres = country_genre_counts[country_genre_counts['country'] == selected_country].nlargest(10, 'count')
        plot_bar(top_genres, 'count', 'genre_1', f"Top Genres in {selected_country}")

# 功能 4: 按导演搜索
elif option == "Search by Director":
    st.header("Search by Director")
    director_name = st.text_input("Enter Director's Name:")
    if director_name:
        matching_directors = sorted(
            {name.strip() for name in df['director'].dropna() if director_name.lower() in name.lower()}
        )
        selected_director = st.selectbox("Select a Director:", matching_directors)
        if selected_director:
            director_movies = df[df['director'].str.contains(selected_director, na=False)]
            display_table(director_movies, {
                'title': 'Title', 'genre_1': 'Genre', 'year': 'Year',
                'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes',
                'rating': 'Rating', 'awards': 'Awards'
            }, f"Movies directed by {selected_director}")

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
