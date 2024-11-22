# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MopaqWhuW-IBe0pPGG6G-OphdtyXSxG7
"""

# 导入库
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
def load_data():
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/94a1553e28a662d831a0d8f224a2e167bdedb204/movies_dataset1.csv"
    return pd.read_csv(url, encoding='ISO-8859-1')

# 数据加载
df = load_data()

# 数据加载
df = load_data()

# 数据概览
print("Dataset Snapshot:")
print(df.head())

# 功能 1: 电影类型分布
genres = pd.concat([df['genre_1'], df['genre_2'], df['genre_3']]).dropna()
genre_counts = genres.value_counts().head(15)

plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis")
plt.title("Top 15 Genres")
plt.xlabel("Count")
plt.ylabel("Genres")
plt.show()

# 功能 2: 按国家和类型
selected_country = "United States"  # 替换为测试的国家
country_data = df[df['country'] == selected_country]
top_genres = pd.concat([country_data['genre_1'], country_data['genre_2'], country_data['genre_3']]).value_counts().head(10)

plt.figure(figsize=(8, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, palette="Blues_r")
plt.title(f"Top Genres in {selected_country}")
plt.xlabel("Count")
plt.ylabel("Genres")
plt.show()

# 功能 3: 按年份评分趋势
rating_trend = df.groupby('year')['imdbRating'].mean().dropna()

plt.figure(figsize=(12, 6))
plt.plot(rating_trend.index, rating_trend.values, marker='o', color='c')
plt.title("Average IMDb Rating Over Time")
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.grid()
plt.show()

# 功能 4: 国家和类型热度图
df_exploded = df.copy()
df_exploded['country'] = df_exploded['country'].str.split(", ")
df_exploded = df_exploded.explode('country')
df_exploded = df_exploded.melt(id_vars=['country'], value_vars=['genre_1', 'genre_2', 'genre_3'], var_name='genre_type', value_name='genre').dropna()

heatmap_data = df_exploded.groupby(['country', 'genre']).size().unstack(fill_value=0).iloc[:15, :15]

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False)
plt.title("Top Genres by Country")
plt.xlabel("Genres")
plt.ylabel("Countries")
plt.show()