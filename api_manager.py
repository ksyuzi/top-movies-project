import requests
import os

MOVIE_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
MOVIE_DETAILS_ENDPOINT = 'https://api.themoviedb.org/3/movie/'
API_KEY = os.environ["API_KEY"]
MOVIE_IMG_URL = 'https://image.tmdb.org/t/p/w500'

# THIS CLASS GETS MOVIE DATA FROM THE API
class ApiManager:
    def get_films_by_title(self, title):
        movie_query = {
            "api_key": API_KEY,
            "query": title,
        }
        response = requests.get(MOVIE_ENDPOINT, params=movie_query)
        response.raise_for_status()
        data = response.json()
        return data['results']

    def get_film_details(self, film_id):
        movie_query = {
            "api_key": API_KEY,
        }
        response = requests.get(f"{MOVIE_DETAILS_ENDPOINT}/{film_id}", params=movie_query)
        response.raise_for_status()
        data = response.json()
        data['poster_url'] = f"{MOVIE_IMG_URL}{data['poster_path']}"
        return data
