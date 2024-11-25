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

# 合并电影类型列并去掉空格
genres = pd.concat([
    df['genre_1'].str.strip(), 
    df['genre_2'].str.strip(), 
    df['genre_3'].str.strip(),
    df['genre_4'].str.strip(),
    df['genre_5'].str.strip()
]).dropna()

#1. 计算类型分布
genre_counts = genres.value_counts()

# 获取前15个类型及其数量
top_15_genres = genre_counts.head(15)

# 将其余类型合并为"Other"
other_count = genre_counts[15:].sum()

# 创建一个新的序列，确保 "Other" 在第十六位
top_15_genres_with_other = pd.concat(
    [top_15_genres, pd.Series({"Other": other_count})]
).iloc[:16]  # 限制最多 16 项

# 显示前15个类型和它们的数量
st.write("Top 15 Genres and Their Counts (with Other):")
st.write(top_15_genres_with_other)

# 为图表重新排列顺序，确保前15个按大小排序，"Other" 在最后
top_15_genres_sorted = pd.concat([
    top_15_genres.sort_values(ascending=False),  # 前15项按降序排序
    pd.Series({"Other": other_count})           # "Other" 放在最后
])

# 显示柱状图
st.bar_chart(top_15_genres_sorted)

# 功能 2: 不同国家电影类型排行
#处理 country 和 genre 列
# 将 country 列拆分成独立的国家
df['country'] = df['country'].str.split(", ")
df_exploded = df.explode('country')  # 展开成多行

# Streamlit App
st.title("Top Genres by Country")

# 用户选择国家
countries = df_exploded['country'].dropna().unique()
selected_country = st.selectbox("Select a Country:", sorted(countries))

# 获取所选国家的 Top 10 Genres
if selected_country:
    country_data = df_exploded[df_exploded['country'] == selected_country]
    top_genres = country_data['genre'].value_counts().head(10)

    # 显示前 10 类型及其数量
    st.write(f"Top 10 Genres in {selected_country}:")
    st.write(top_genres)

    # 绘制柱状图
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax, palette="viridis")
    ax.set_title(f"Top 10 Genres in {selected_country}")
    ax.set_xlabel("Count")
    ax.set_ylabel("Genre")
    st.pyplot(fig)
