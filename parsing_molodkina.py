import requests
from bs4 import BeautifulSoup

def get_movies_info(url):
    response = requests.get(url)

    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')

        
        movie_titles = soup.find_all('span', class_='text text_block text_fixed text_light_large')
        movie_ratings_site = soup.find_all('span', class_='p-rate-flag__text')
        movie_ratings_imdb = soup.find_all('span', class_='p-rate-flag__imdb-text')
        movie_genres_countries = soup.find_all('a', class_='color_black underline')
        movies_info = []

     
        for i in range(len(movie_titles)):
            title = movie_titles[i].get_text(strip=True)
            rating_site = movie_ratings_site[i].get_text(strip=True)
            rating_imdb = movie_ratings_imdb[i].get_text(strip=True)
            genre = movie_genres_countries[i * 2].get_text(strip=True)
            country = movie_genres_countries[i * 2 + 1].get_text(strip=True)

            
            movies_info.append({
                'title': title,
                'rating_site': rating_site,
                'rating_imdb': rating_imdb,
                'genre': genre,
                'country': country
            })

        return movies_info
    else:
        print(f"Ошибка при получении страницы: {response.status_code}")

    return []

def main():
    url = 'https://kino.mail.ru/cinema/top/'
    movies_info = get_movies_info(url)

    
    for movie in movies_info:
        print(f"Наименование: {movie['title']}, Рейтинг от сайта: {movie['rating_site']}, Рейтинг от IMDb: {movie['rating_imdb']}, Жанр: {movie['genre']}, Страна: {movie['country']}")

if __name__ == "__main__":
    main()