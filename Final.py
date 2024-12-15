import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

#load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Mhu0824/Streamlit/d6d8457d63867b435bfdea9c541afd71495829f9/movies_dataset.csv"
    return pd.read_csv(url, encoding='ISO-8859-1')

df = load_data()

df['year'] = df['year'].astype(str).str.replace(r'\D', '', regex=True)
df_cleaned = df.drop_duplicates()

# title
st.title("🎬 Movie Data Dashboard")

# Choose a function
option = st.sidebar.radio(
    "Choose a feature:",
    ("Overview", "Genre Distribution", "Top Genres by Country", "Search by Director", "Search by Movie", "Unearth Hidden Movies: Rate & Vote","Compare Movie Rating to Genre Average")
)

# Feature 1: Overview
if option == "Overview":
    st.header("Overview")
    st.write("""
        Welcome to the Movie Data Explorer! This dashboard allows you to explore various aspects of a large movie dataset, 
        including insights into movie genres, ratings, countries, directors, and more. Below is an overview of the key features you can explore:
        
        - **Genre Distribution**: Explore the distribution of movie genres across the dataset, highlighting the most common genres.
        
        - **Top Genres by Country**: Discover the top genres of movies based on country, helping to identify regional preferences.
        
        - **Search by Director**: Look up movies by specific directors, view their movie details, and explore their average ratings.
        
        - **Search by Movie**: Find movies by title, get details about the selected movie, and explore other works by the same director.
        
        - **Unearth Hidden Movies: Rate & Vote**: Filters movies based on user-defined IMDb ratings and vote ranges to help discover hidden gems(highly rated movies with fewer votes, which might have been overlooked by a wider audience).
        
        - **Compare Movie Rating to Genre Average**: Compares a movie’s rating to its genre's average rating. It shows how the movie fares against similar films, helping users identify underrated or overrated movies within the same genre.
    """)

# Feature 2: Genre Distribution
elif option == "Genre Distribution":
    st.header("Genre Distribution")

    # Process movie genre data
    genres = pd.concat([
        df['genre_1'].str.strip(), 
        df['genre_2'].str.strip(), 
        df['genre_3'].str.strip(),
        df['genre_4'].str.strip(),
        df['genre_5'].str.strip()
    ]).dropna()

    # Calculate the distribution of all genres
    genre_counts = genres.value_counts()

    # Display all genres and their counts
    st.write("All Genres and Their Counts:")
    st.write(genre_counts)

    # Get the top 15 genres and thier counts
    top_15_genres = genre_counts.head(15)

    # Combine remaining genres as "Other"
    other_count = genre_counts[15:].sum()

    # Create a new series adding "Other" to the top 15 genres
    top_15_genres_with_other = pd.concat(
        [top_15_genres, pd.Series({"Other": other_count})]
    )

    # Display a bar chart
    st.header("Top 15 Genres and 'Other'")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_15_genres_with_other.values, y=top_15_genres_with_other.index, ax=ax)
    ax.set_title("Top 15 Genres and 'Other'")
    st.pyplot(fig)

# Feature 3: Movie genres by country
elif option == "Top Genres by Country":
    # Split the country column
    df['country'] = df['country'].str.split(", ")
    df_exploded = df.explode('country')  # Expand to multiple rows, one per country

    # Use only genre_1 content
    df_exploded = df_exploded[['country', 'genre_1']].dropna()
    df_exploded['genre_1'] = df_exploded['genre_1'].str.strip()  # Remove whitespace

    # Count by country and genre_1
    country_genre_counts = df_exploded.groupby(['country', 'genre_1']).size().reset_index(name='count')

    # User selects a country
    countries = country_genre_counts['country'].unique()
    selected_country = st.selectbox("Select a Country:", sorted(countries))

    # Get the top 10 genres for the selected country
    if selected_country:
        top_genres = country_genre_counts[country_genre_counts['country'] == selected_country]
        top_genres = top_genres.nlargest(10, 'count')

        # Rename columns
        top_genres_display = top_genres[['genre_1', 'count']].rename(columns={'genre_1': 'Genre', 'count': 'Count'}).reset_index(drop=True)

        # Display the top 10 genres and their counts
        st.write(f"Top 10 Genres for {selected_country}:")
        st.write(top_genres_display)

        # Plot a bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='Count', y='Genre', data=top_genres_display, ax=ax)
        ax.set_title(f"Top Genres in {selected_country}")
        st.pyplot(fig)

# Feature 4: Search by director name
elif option == "Search by Director":
    st.header("Search by Director")

    # User inputs a director's name with auto-matching suggestions
    director_name = st.text_input("Enter Director's Name:")
    if director_name:
        matching_directors = sorted(
            {name.strip() for name in df['director'].dropna() if director_name.lower() in name.lower()}
        )
        selected_director = st.selectbox("Select a Director:", matching_directors)
        
        if selected_director:
            # Filter movies by the director
            director_movies = df[df['director'].str.contains(selected_director, na=False)]
            
            # Display movies by the director and relevant information
            st.write(f"Movies directed by {selected_director}:")
            st.dataframe(
                director_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                    columns={
                        'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                        'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes', 
                        'rating': 'Rating', 'awards': 'Awards'
                    }
                )
            )

            # Calculate the average rating for the director's movies
            avg_rating = director_movies['imdbRating'].mean()
            st.write(f"Average IMDB Rating for {selected_director}'s movies: {avg_rating:.2f}")

# Feature 5: Search by Movie
elif option == "Search by Movie":
    st.header("Search by Movie")

    # User enters the movie title, with suggestions showing results (including year)
    movie_name = st.text_input("Enter Movie Title:")

    if movie_name:
        # Clean the title and year columns in the dataset
        df['title_clean'] = df['title'].str.strip().str.lower() 
        df['year_clean'] = df['year'].astype(str).str.strip()  # Ensure year is a string and strip spaces

        # Get all movies matching the entered name, displaying movie names with their release years
        matching_movies = sorted(
            {f"{title.strip()} ({year})" for title, year in zip(df['title_clean'], df['year_clean']) 
             if pd.notna(title) and movie_name.lower() in title.lower()}
        )
        
        # Display all matching movie names (with years)
        if matching_movies:
            selected_movie_with_year = st.selectbox("Select a Movie:", matching_movies)
            
            if selected_movie_with_year:
                # Parse the movie title and year from the selection
                selected_movie, selected_year = selected_movie_with_year.rsplit(" (", 1)
                selected_year = selected_year.rstrip(")")
                
                # Filter the dataset for the unique movie using title_clean and year_clean
                movie_details = df[(df['title_clean'] == selected_movie.lower()) & (df['year_clean'] == selected_year)]
                
                if not movie_details.empty:
                    # Get the director's name
                    director_name = movie_details['director'].iloc[0]
                    
                    # Display detailed information
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
                    
                    # Display other movies by the same director
                    other_movies = df[df['director'] == director_name]
                    st.write(f"Other movies by {director_name}:")
                    st.dataframe(
                        other_movies[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                            columns={
                                'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                                'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes',
                                'rating': 'Rating', 'awards': 'Awards'
                            }
                        )
                    )
                    
                    # Calculate the average rating of other movies by the director
                    avg_rating = other_movies['imdbRating'].mean()
                    st.write(f"Average IMDB Rating for {director_name}'s movies: {avg_rating:.2f}")
                else:
                    st.write("No movie details found for the selected movie.")
        else:
            st.write("No matching movies found.")
            
# Feature 6: Unearth Hidden Movies
elif option == "Unearth Hidden Movies: Rate & Vote":
    st.header("Unearth Hidden Movies: Rate & Vote")
    
    # Select a genre
    st.subheader("Step 1: Select Genre (Optional)")
    genre = st.selectbox(
        "Select a Genre (Leave empty for all genres):", 
        options=["All"] + sorted(df['genre_1'].dropna().unique()),  # Includes the "All" option
        index=0  # Defaults to "All"
    )
    
    # Allow users to define a range for votes
    st.subheader("Step 2: Select IMDB Votes Range")
    min_votes = st.number_input("Minimum Votes", min_value=0, max_value=2000000, value=0, step=100)
    max_votes = st.number_input("Maximum Votes", min_value=0, max_value=2000000, value=1000, step=100)
    
    # Allow users to set a range for ratings
    st.subheader("Step 3: Customize Your Rating Range")
    rating_filter = st.slider(
        "Select IMDB Rating Range", 
        min_value=0.0, max_value=10.0, 
        value=(7.0, 10.0),  # Default range
        step=0.1  # Step size for ratings
    )
    
    # Filter and display the data
    filtered_movies = df[
        ((df['genre_1'] == genre) | (genre == "All")) &  # Filter by genre if specified, otherwise show all genres
        (df['imdbVotes'] >= min_votes) & 
        (df['imdbVotes'] <= max_votes) & 
        (df['imdbRating'] >= rating_filter[0]) & 
        (df['imdbRating'] <= rating_filter[1])
    ]
    filtered_movies_sorted = filtered_movies.sort_values(by='imdbRating', ascending=False)

    # Display the filtered results
    st.write(
        f"Movies in {genre if genre != 'All' else 'all genres'} with IMDB Votes between {min_votes} and {max_votes}, "
        f"and IMDB Rating between {rating_filter[0]} and {rating_filter[1]}:"
    )
    st.dataframe(
        filtered_movies_sorted[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes']].rename(
            columns={
                'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes'
            }
        )
    )
    
    # Show hidden gems
    st.subheader("What This Can Do: Discover Your Hidden Gems")
    hidden_gems = df[
        ((df['genre_1'] == genre) | (genre == "All")) &  # Also supports filtering by genre or all genres
        (df['imdbVotes'] < 1000) & 
        (df['imdbRating'] > 7.0)
    ]
    hidden_gems_sorted = hidden_gems.sort_values(by='imdbRating', ascending=False)
    
    if not hidden_gems_sorted.empty:
        st.write(
            "For example, here are some *Hidden Gems* (highly rated movies(>7.0) with less than 1000 votes):"
        )
        st.dataframe(
            hidden_gems_sorted[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes']].rename(
                columns={
                    'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                    'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes'
                }
            )
        )
    else:
        st.write(f"No hidden gems found in {genre if genre != 'All' else 'all genres'}.")

# Feature 7: Compare Movie Rating to Dataset Average
elif option == "Compare Movie Rating to Genre Average":
    st.header("Compare Movie Rating to Genre Average")

    # User inputs movie title
    movie_name = st.text_input("Enter Movie Title:")

    if movie_name:
        # Ensure necessary columns are cleaned and available
        if 'title_clean' not in df.columns:
            df['title_clean'] = df['title'].str.strip().str.lower()  # Clean 'title' column
        if 'year_clean' not in df.columns:
            df['year_clean'] = df['year'].astype(str).str.strip()  # Clean 'year' column and ensure it's a string

        # Find matching movies based on the entered title
        matching_movies = sorted(
            {f"{title} ({year})" for title, year in zip(df['title'], df['year']) 
             if pd.notna(title) and movie_name.lower() in title.lower()}
        )

        if matching_movies:
            # Allow user to select a movie from the matching options
            selected_movie_with_year = st.selectbox("Select a Movie:", matching_movies)

            if selected_movie_with_year:
                # Extract the selected movie's title and year
                selected_movie, selected_year = selected_movie_with_year.rsplit(" (", 1)
                selected_year = selected_year.rstrip(")")

                # Filter the dataset to find the selected movie
                movie_details = df[
                    (df['title_clean'] == selected_movie.strip().lower()) &
                    (df['year_clean'] == selected_year)
                ]

                if not movie_details.empty:
                    st.write(f"Selected Movie: **{selected_movie} ({selected_year})**")
                    st.dataframe(
                        movie_details[['title', 'genre_1', 'year', 'imdbRating', 'imdbVotes', 'rating', 'awards']].rename(
                            columns={
                                'title': 'Title', 'genre_1': 'Genre', 'year': 'Year', 
                                'imdbRating': 'IMDB Rating', 'imdbVotes': 'IMDB Votes', 
                                'rating': 'Rating', 'awards': 'Awards'
                            }
                        )
                    )

                    # Get the IMDB rating of the selected movie
                    movie_rating = movie_details['imdbRating'].iloc[0]

                    # Calculate the average IMDB rating for the entire dataset
                    dataset_avg_rating = df['imdbRating'].mean()

                    # Visualize the comparison
                    try:
                        # Prepare data for the bar chart
                        fig = go.Figure()

                        # Add a bar for the dataset average rating
                        fig.add_trace(go.Bar(
                            x=["Dataset Average"],
                            y=[dataset_avg_rating],
                            name="Dataset Average Rating",
                            marker=dict(color='rgba(58, 71, 80, 0.7)'),  # Set bar color
                            opacity=0.7  # Set transparency
                        ))

                        # Add a bar for the selected movie's rating
                        fig.add_trace(go.Bar(
                            x=["Selected Movie"],
                            y=[movie_rating],
                            name="Selected Movie Rating",
                            marker=dict(color='rgba(255, 99, 71, 0.7)'),  # Set bar color
                            opacity=0.7  # Set transparency
                        ))

                        # Update chart layout for better readability
                        fig.update_layout(
                            title=f"Rating Comparison for '{selected_movie} ({selected_year})'",
                            xaxis_title="Category",
                            yaxis_title="Rating",
                            showlegend=True,
                            barmode='group',  # Grouped bar chart
                            template="plotly_dark",  # Set background theme
                        )

                        # Display the chart
                        st.plotly_chart(fig)

                    except Exception as e:
                        st.error(f"Error creating chart: {e}")
                else:
                    st.error("No matching movie found with the given title and year.")
        else:
            st.warning("No matching movies found for the entered title.")
    else:
        st.warning("Please enter a movie title to begin the search.")
