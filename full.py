import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
@st.cache
def load_data():
    # 使用GitHub上的CSV文件链接或本地文件路径
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/0cf50d29b8420dec4063fac0a9641bd68a9b28f0/movies_dataset1.csv"
    return pd.read_csv(url, encoding='ISO-8859-1')

# 数据加载
df = load_data()

# 标题
st.title("🎬 Movie Data Dashboard")

# 数据概览
st.header("Overview")
st.write("Dataset Snapshot:")
st.dataframe(df.head())

# 功能 1: 电影类型分布
st.header("Genre Distribution")
genres = pd.concat([df['genre_1'], df['genre_2'], df['genre_3']]).dropna()
genre_counts = genres.value_counts().head(15)

st.bar_chart(genre_counts)

# 功能 2: 按国家和类型
st.header("Top Genres by Country")
selected_country = st.selectbox("Select a Country", df['country'].unique())
country_data = df[df['country'] == selected_country]
top_genres = pd.concat([country_data['genre_1'], country_data['genre_2'], country_data['genre_3'], country_data['genre_4'], country_data['genre_5']]).value_counts().head(10)

st.write(f"Top 10 Genres for {selected_country}:")
st.write(top_genres)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)
ax.set_title(f"Top Genres in {selected_country}")
st.pyplot(fig)

# 功能 3: 按年份评分趋势
st.header("Ratings Over Time")
rating_trend = df.groupby('year')['imdbRating'].mean().dropna()

st.line_chart(rating_trend)

# 功能 4: 国家和类型热度图
st.header("Genre Heatmap by Country")
df_exploded = df.copy()
df_exploded['country'] = df_exploded['country'].str.split(", ")
df_exploded = df_exploded.explode('country')
df_exploded = df_exploded.melt(id_vars=['country'], value_vars=['genre_1', 'genre_2', 'genre_3'], var_name='genre_type', value_name='genre').dropna()

heatmap_data = df_exploded.groupby(['country', 'genre']).size().unstack(fill_value=0).iloc[:15, :15]

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
ax.set_title("Top Genres by Country")
st.pyplot(fig)
