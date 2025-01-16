import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def get_movies_info(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        movie_titles = soup.find_all('span', class_='text text_block text_fixed text_light_large')
        movie_ratings_site = soup.find_all('span', class_='p-rate-flag__text')
        movie_ratings_imdb = soup.find_all('span', class_='p-rate-flag__imdb-text')
        movie_genres_countries = soup.find_all('div', class_='margin_top_5')
        movies_info = []

        for i in range(len(movie_titles)):
            title = movie_titles[i].get_text(strip=True)
            rating_site = movie_ratings_site[i].get_text(strip=True)
            rating_imdb = movie_ratings_imdb[i].get_text(strip=True)
            genre_country_year = movie_genres_countries[i].get_text(strip=True)

            
            parts = genre_country_year.split(',')
            genre = parts[0].strip()
            country = parts[1].strip()
            year = parts[2].strip()

            movies_info.append({
                'title': title,
                'rating_site': rating_site,
                'rating_imdb': rating_imdb,
                'genre': genre,
                'country': country,
                'year': year
            })

        return movies_info
    else:
        print(f"Ошибка при получении страницы: {response.status_code}")

    return []

def main():
    url = 'https://kino.mail.ru/cinema/top/'
    movies_info = get_movies_info(url)

    
    df = pd.DataFrame(movies_info)

    
    print(df)

    
    high_rated_movies_8 = df[df['rating_site'].astype(float) > 8]

    
    genre_counts_8 = high_rated_movies_8['genre'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(genre_counts_8, labels=genre_counts_8.index, autopct='%1.1f%%', startangle=140)
    plt.title('Жанры фильмов с рейтингом сайта больше 8')
    plt.legend(genre_counts_8.index, title="Жанры", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()

 

if __name__ == "__main__":
    main()