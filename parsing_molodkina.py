import requests
from bs4 import BeautifulSoup
import pandas as pd

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

            # Разделяем строку на жанр, страну и год
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

    # Преобразуем список словарей в DataFrame
    df = pd.DataFrame(movies_info)

    # Выводим DataFrame на экран
    print(df)

if __name__ == "main":
    main()