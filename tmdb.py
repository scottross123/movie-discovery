"""
Contains functions that interact witht TMDB API
"""

import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your API keys from .env

movie_id = "585245"

KEY = os.getenv("KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/"

def get_movie(id):
    url = BASE_URL + id

    # create request
    r = requests.get(url, params={"api_key": KEY})

    # convert request to json
    r_json = r.json()
    name = ""
    desc = (r_json["title"], r_json["tagline"], [d["name"] for d in r_json["genres"]]) 

    return desc

def get_movie_image(id):
    

print(get_movie(movie_id))

