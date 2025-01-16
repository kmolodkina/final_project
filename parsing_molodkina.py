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

    # Фильтруем фильмы с рейтингом сайта больше 8
    high_rated_movies_8 = df[df['rating_site'].astype(float) > 8]

    # Круговая диаграмма для жанров фильмов с рейтингом сайта больше 8
    genre_counts_8 = high_rated_movies_8['genre'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(genre_counts_8, labels=genre_counts_8.index, autopct='%1.1f%%', startangle=140)
    plt.title('Страны фильмов с рейтингом сайта больше 8')
    plt.legend(genre_counts_8.index, title="Страны", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()

    # Фильтруем фильмы с рейтингом сайта больше 9
    high_rated_movies_9 = df[df['rating_imdb'].astype(float) > 9]

    # Круговая диаграмма для стран фильмов с рейтингом сайта больше 9
    country_counts_9 = high_rated_movies_9['country'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(country_counts_9, labels=country_counts_9.index, autopct='%1.1f%%', startangle=140)
    plt.title('Года фильмов с рейтингом сайта больше 9')
    plt.legend(country_counts_9.index, title="Года", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()

    # График изменения оценок фильмов с годами (первые 10 фильмов)
    first_10_movies = df.head(10)
    years = first_10_movies['country'].astype(int)  # Используем переменную country для годов
    ratings = first_10_movies['rating_site'].astype(float)

    plt.figure(figsize=(10, 6))
    plt.plot(years, ratings, marker='o', linestyle='-', color='b')
    plt.title('Изменение оценок фильмов с годами')
    plt.xlabel('Год')
    plt.ylabel('Оценка')
    plt.grid(True)
    plt.show()

if name == "main":
    main()