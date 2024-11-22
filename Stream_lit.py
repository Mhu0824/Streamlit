{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNQNRhKCKqzPNViaKNFiKG0",
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
        "<a href=\"https://colab.research.google.com/github/Mhu0824/Streamlit/blob/main/Stream_lit.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 378
        },
        "id": "Bwdu_NwOLTFG",
        "outputId": "dc6a19c9-49d0-41bc-96dc-c1d184d1a9c4"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-b60b356ec9a0>\u001b[0m in \u001b[0;36m<cell line: 1>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mmatplotlib\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpyplot\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mplt\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mseaborn\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0msns\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "import gdown\n",
        "\n",
        "file_id = '1-fHxuVWiMsxD2Q12tpowl_enf8kFXD94'\n",
        "gdown.download(f'https://drive.google.com/uc?id={file_id}', 'movies_dataset.csv', quiet=False)\n",
        "\n",
        "df = pd.read_csv('movies_dataset.csv', encoding='ISO-8859-1')\n",
        "# 读取数据\n",
        "@st.cache\n",
        "def load_data():\n",
        "    return pd.read_csv(\"movies_dataset.csv\", encoding='ISO-8859-1')\n",
        "\n",
        "df = load_data()\n",
        "\n",
        "# 标题\n",
        "st.title(\"Movie Data Dashboard\")\n",
        "\n",
        "# 数据概览\n",
        "st.header(\"Overview\")\n",
        "st.write(\"Dataset Snapshot:\")\n",
        "st.dataframe(df.head())\n",
        "\n",
        "# 功能 1: 电影类型分布\n",
        "st.header(\"Genre Distribution\")\n",
        "genres = pd.concat([df['genre_1'], df['genre_2'], df['genre_3']]).dropna()\n",
        "genre_counts = genres.value_counts().head(15)\n",
        "\n",
        "st.bar_chart(genre_counts)\n",
        "\n",
        "# 功能 2: 按国家和类型\n",
        "st.header(\"Top Genres by Country\")\n",
        "selected_country = st.selectbox(\"Select a Country\", df['country'].unique())\n",
        "country_data = df[df['country'] == selected_country]\n",
        "top_genres = pd.concat([country_data['genre_1'], country_data['genre_2'], country_data['genre_3']]).value_counts().head(10)\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(8, 6))\n",
        "sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)\n",
        "ax.set_title(f\"Top Genres in {selected_country}\")\n",
        "st.pyplot(fig)\n",
        "\n",
        "# 功能 3: 按年份评分趋势\n",
        "st.header(\"Ratings Over Time\")\n",
        "rating_trend = df.groupby('year')['imdbRating'].mean().dropna()\n",
        "\n",
        "st.line_chart(rating_trend)"
      ]
    }
  ]
}
