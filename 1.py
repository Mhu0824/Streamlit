{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNRb79drf/j2VJ3ZdiVpKu0",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Mhu0824/Streamlit/blob/main/1.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 7,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 207
        },
        "id": "Bwdu_NwOLTFG",
        "outputId": "35999557-4656-44ea-b62b-2961fc83b9c6"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "NameError",
          "evalue": "name 'st' is not defined",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-7-e7e18a25f581>\u001b[0m in \u001b[0;36m<cell line: 6>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;31m# 读取数据\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 6\u001b[0;31m \u001b[0;34m@\u001b[0m\u001b[0mst\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcache\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      7\u001b[0m \u001b[0;32mdef\u001b[0m \u001b[0mload_data\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      8\u001b[0m     \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mNameError\u001b[0m: name 'st' is not defined"
          ]
        }
      ],
      "source": [
        "import pandas as pd\n",
        "import streamlit as st\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "# 读取数据\n",
        "@st.cache\n",
        "def load_data():\n",
        "    try:\n",
        "        return pd.read_csv(\"movies_dataset1.csv\", encoding='ISO-8859-1')\n",
        "    except FileNotFoundError:\n",
        "        st.error(\"File not found! Make sure the dataset is uploaded.\")\n",
        "\n",
        "df = load_data()\n",
        "\n",
        "if df is not None:\n",
        "    # 标题\n",
        "    st.title(\"Movie Data Dashboard\")\n",
        "\n",
        "    # 数据概览\n",
        "    st.header(\"Overview\")\n",
        "    st.write(\"Dataset Snapshot:\")\n",
        "    st.dataframe(df.head())\n",
        "\n",
        "    # 功能 1: 电影类型分布\n",
        "    st.header(\"Genre Distribution\")\n",
        "    genres = pd.concat([df['genre_1'], df['genre_2'], df['genre_3']]).dropna()\n",
        "    genre_counts = genres.value_counts().head(15)\n",
        "\n",
        "    st.bar_chart(genre_counts)\n",
        "\n",
        "    # 功能 2: 按国家和类型\n",
        "    st.header(\"Top Genres by Country\")\n",
        "    selected_country = st.selectbox(\"Select a Country\", df['country'].unique())\n",
        "    country_data = df[df['country'] == selected_country]\n",
        "    top_genres = pd.concat([country_data['genre_1'], country_data['genre_2'], country_data['genre_3']]).value_counts().head(10)\n",
        "\n",
        "    fig, ax = plt.subplots(figsize=(8, 6))\n",
        "    sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)\n",
        "    ax.set_title(f\"Top Genres in {selected_country}\")\n",
        "    st.pyplot(fig)\n",
        "\n",
        "    # 功能 3: 按年份评分趋势\n",
        "    st.header(\"Ratings Over Time\")\n",
        "    rating_trend = df.groupby('year')['imdbRating'].mean().dropna()\n",
        "\n",
        "    st.line_chart(rating_trend)"
      ]
    }
  ]
}