# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MopaqWhuW-IBe0pPGG6G-OphdtyXSxG7
"""

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
st.header("All Genres and Their Counts")
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
st.bar_chart(top_15_genres_with_other)

#2.不同国家电影类型
# 拆分 `country` 列
df['country'] = df['country'].str.split(", ")
df_exploded = df.explode('country')  # 展开成多行，每行一个国家

# 只使用 `genre_1` 的内容
df_exploded = df_exploded[['country', 'genre_1']].dropna()
df_exploded['genre_1'] = df_exploded['genre_1'].str.strip()  # 去掉空格

# 按国家和 `genre_1` 统计
country_genre_counts = df_exploded.groupby(['country', 'genre_1']).size().reset_index(name='count')

# Streamlit 界面
st.title("Top Genres by Country (Using genre_1)")

# 用户选择国家
countries = country_genre_counts['country'].unique()
selected_country = st.selectbox("Select a Country:", sorted(countries))

# 获取所选国家的 Top 10 类型
if selected_country:
    top_genres = country_genre_counts[country_genre_counts['country'] == selected_country]
    top_genres = top_genres.nlargest(10, 'count')

    # 重命名列为“Count”和“Genre”
    top_genres_display = top_genres[['genre_1', 'count']].rename(columns={'genre_1': 'Genre', 'count': 'Count'})

    # 显示Top 10类型及其数量
    st.write(f"Top 10 Genres for {selected_country}:")
    st.write(top_genres_display)

    # 绘制条形图
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Count', y='Genre', data=top_genres_display, ax=ax)
    ax.set_title(f"Top Genres in {selected_country}")
    st.pyplot(fig)
