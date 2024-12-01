import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config at the beginning
st.set_page_config(page_title="Movie Data Dashboard", layout="wide")

# 加载数据
@st.cache
def load_data():
    # 使用GitHub上的CSV文件链接或本地文件路径
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/d6d8457d63867b435bfdea9c541afd71495829f9/movies_dataset.csv"
    return pd.read_csv(url, encoding='ISO-8859-1')

df = load_data()

df['year'] = df['year'].astype(str).str.replace(r'\D', '', regex=True)

# 标题
st.title("🎬 Movie Data Dashboard")

# 功能选择
option = st.sidebar.radio(
    "Choose a feature:",
    ("Overview", "Genre Distribution", "Top Genres by Country", "Search by Director", "Search by Movie", "Hidden Gems")
)

# 功能 1: 数据概览
if option == "Overview":
    st.header("Overview")
    st.write("Dataset Snapshot:")
    st.dataframe(df.head())

# 功能 2: 电影类型分布
elif option == "Genre Distribution":
    st.header("Genre Distribution")

    # 处理电影类型数据
    genres = pd.concat([
        df['genre_1'].str.strip(), 
        df['genre_2'].str.strip(), 
        df['genre_3'].str.strip(),
        df['genre_4'].str.strip(),
        df['genre_5'].str.strip()
    ]).dropna()

    # 计算所有类型的分布
    genre_counts = genres.value_counts()

    # 在 Streamlit 中显示所有类型及其数量
    st.write("All Genres and Their Counts:")
    st.write(genre_counts)

    # 获取前 15 个类型及其数量
    top_15_genres = genre_counts.head(15)

    # 将其余类型合并为 "Other"
    other_count = genre_counts[15:].sum()

    # 创建一个新的序列，将 "Other" 直接添加到前 15 个类型中
    top_15_genres_with_other = pd.concat(
        [top_15_genres, pd.Series({"Other": other_count})]
    )

    # 显示柱状图
    st.header("Top 15 Genres and 'Other'")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_15_genres_with_other.values, y=top_15_genres_with_other.index, ax=ax)
    ax.set_title("Top 15 Genres and 'Other'")
    st.pyplot(fig)

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
        top_genres = country_genre_counts[country_genre_counts['country'] == selected_country]
        top_genres = top_genres.nlargest(10, 'count')
        top_genres_display = top_genres[['genre_1', 'count']].rename(columns={'genre_1': 'Genre', 'count': 'Count'})

        st.write(f"Top 10 Genres for {selected_country}:")
        st.write(top_genres_display)

        # 绘制条形图
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='Count', y='Genre', data=top_genres_display, ax=ax, palette="viridis")
        ax.set_title(f"Top Genres in {selected_country}")
        st.pyplot(fig)

# 功能 4: 按导演名字搜索
elif option == "Search by Director":
    st.header("🔍 Search by Director")
    director_name = st.text_input("Enter Director's Name:")

    if director_name:
        matching_directors = sorted(
            {name.strip() for name in df['director'].dropna() if director_name.lower() in name.lower()}
        )
        selected_director = st.selectbox("Select a Director:", matching_directors)
        
        if selected_director:
            director_movies = df[df['director'].str.contains(selected_director, na=False)]
            st.write(f"Movies directed by {selected_director}:")
            st.dataframe(
                director_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                    columns={'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 'imdbRating': 'IMDB Rating', 
                             'imdbVotes': 'IMDB Votes', 'rating': 'Rating', 'awards': 'Awards'}
                )
            )

            avg_rating = director_movies['imdbRating'].mean()
            st.write(f"Average IMDB Rating for {selected_director}'s movies: {avg_rating:.2f}")

# 功能 5: 按电影名字搜索
elif option == "Search by Movie":
    st.header("🔍 Search by Movie")
    movie_name = st.text_input("Enter Movie Title:")

    if movie_name:
        df['title_clean'] = df['title'].str.strip().str.lower()
        df['year_clean'] = df['year'].astype(str).str.strip()
        
        matching_movies = sorted(
            {f"{title.strip()} ({year})" for title, year in zip(df['title_clean'], df['year_clean']) 
             if pd.notna(title) and movie_name.lower() in title.lower()}
        )
        
        if matching_movies:
            selected_movie_with_year = st.selectbox("Select a Movie:", matching_movies)
            
            if selected_movie_with_year:
                selected_movie, selected_year = selected_movie_with_year.rsplit(" (", 1)
                selected_year = selected_year.rstrip(")")

                movie_details = df[(df['title_clean'] == selected_movie.lower()) & (df['year_clean'] == selected_year)]

                if not movie_details.empty:
                    director_name = movie_details['director'].iloc[0]
                    st.write(f"Details for '{selected_movie} ({selected_year})' created by {director_name}:")
                    st.dataframe(
                        movie_details[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                            columns={'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 'imdbRating': 'IMDB Rating', 
                                     'imdbVotes': 'IMDB Votes', 'rating': 'Rating', 'awards': 'Awards'}
                        )
                    )

                    other_movies = df[df['director'] == director_name]
                    st.write(f"Other movies by {director_name}:")
                    st.dataframe(
                        other_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                            columns={'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 'imdbRating': 'IMDB Rating', 
                                     'imdbVotes': 'IMDB Votes', 'rating': 'Rating', 'awards': 'Awards'}
                        )
                    )

                    avg_rating = other_movies['imdbRating'].mean()
                    st.write(f"Average IMDB Rating for {director_name}'s movies: {avg_rating:.2f}")
                else:
                    st.write("No movie details found for the selected movie.")
        else:
            st.write("No matching movies found.")

# 功能 6: 冷门佳作
elif option == "Hidden Gems":
    st.header("💎 Hidden Gems: High Ratings but Low Votes")
    genre = st.selectbox("Select Genre:", sorted(df['genre_1'].dropna().unique()))
    
    if genre:
        hidden_gems = df[(df['genre_1'] == genre) & (df['imdbVotes'] < 1000) & (df['imdbRating'] >= 7.5)]
        hidden_gems_sorted = hidden_gems.sort_values(by='imdbRating', ascending=False)

        if not hidden_gems_sorted.empty:
            st.write(f"Hidden Gems in {genre}:")
            st.dataframe(
                hidden_gems_sorted[['title', 'year', 'imdbRating', 'imdbVotes']].rename(
                    columns={'title': 'Title', 'year': 'Year', 'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes'}
                )
            )
        else:
            st.write(f"No hidden gems found for {genre}.")
