import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

spotify_data = pd.read_csv(r'C:\Users\einavl\OneDrive - weizmann.ac.il\Desktop\Weizmann Institute of Science\Python_course_2025\WIS-python-assignments-2025\Day8\spotify_2015_2025_85k.csv')
# print(spotify_data.head())

latin_countries = ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']

latin_songs=spotify_data[spotify_data['country'].isin(latin_countries)]
# print(latin_songs.head())
# print(len(latin_songs))
# print(latin_songs[['track_name', 'artist_name', 'country', 'explicit']])

latin_songs = latin_songs.sort_values(by='country', ascending=True)
# print(latin_songs[['track_name', 'artist_name', 'country', 'explicit']])

argentinian_songs=latin_songs[latin_songs['country']=='Argentina']
print(argentinian_songs[['track_name', 'artist_name', 'country', 'explicit']])

countries = spotify_data['country'].unique()
print(countries)    

##plot correlation between country and explicit
explicit_songs_country= spotify_data.groupby('country')['explicit'].sum()
print(explicit_songs_country)

plt.scatter(explicit_songs_country.index, explicit_songs_country.values)

# Calculate regression
x_numeric = np.arange(len(explicit_songs_country))
slope, intercept, r_value, p_value, std_err = stats.linregress(x_numeric, explicit_songs_country.values)
regression_line = slope * x_numeric + intercept
r_squared = r_value**2

# Plot regression line
plt.plot(explicit_songs_country.index, regression_line, color='red', label=f'R²={r_squared:.2f}, p={p_value:.4f}')
plt.legend()
plt.xticks(rotation=90) # Rotate x-labels for better readability since there are many countries
plt.show()

spotify_data['release_date'] = pd.to_datetime(spotify_data['release_date'])
spotify_data['year'] = spotify_data['release_date'].dt.year

avg_year_by_country = spotify_data.groupby('country')['year'].mean()
print(avg_year_by_country)
plt.bar(avg_year_by_country.index, avg_year_by_country.values)
plt.title("Average Year of Release by Country")
plt.xticks(rotation=90)
plt.show()

# Genre Popularity Analysis
avg_popularity_by_genre = spotify_data.groupby('genre')['popularity'].mean().sort_values(ascending=False)
print(avg_popularity_by_genre)
plt.bar(avg_popularity_by_genre.index, avg_popularity_by_genre.values)
plt.title("Average Popularity by Genre")
plt.xticks(rotation=90)
plt.ylabel("Popularity")
plt.show()

# Tempo Trends Over Time
avg_tempo_by_year = spotify_data.groupby('year')['tempo'].mean()
print(avg_tempo_by_year)
plt.plot(avg_tempo_by_year.index, avg_tempo_by_year.values, marker='o')
plt.title("Average Tempo Trends Over Time")
plt.xlabel("Year")
plt.ylabel("Tempo (BPM)")
plt.grid(True)
plt.show()

# Explicit vs Popularity Analysis
avg_popularity_by_explicit = spotify_data.groupby('explicit')['popularity'].mean()
print(avg_popularity_by_explicit)
plt.bar(avg_popularity_by_explicit.index.astype(str), avg_popularity_by_explicit.values)
plt.title("Average Popularity: Explicit vs Non-Explicit")
plt.xlabel("Explicit (0=No, 1=Yes)")
plt.ylabel("Popularity")
plt.show()

# Country Danceability Analysis
avg_danceability_by_country = spotify_data.groupby('country')['danceability'].mean().sort_values(ascending=False)
print(avg_danceability_by_country)
plt.bar(avg_danceability_by_country.index, avg_danceability_by_country.values)
plt.title("Average Danceability by Country")
plt.xticks(rotation=90)
plt.ylabel("Danceability")
plt.show()