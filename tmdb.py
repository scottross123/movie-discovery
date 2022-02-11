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
    desc = (r_json["title"], r_json["tagline"], [d["name"] for d in r_json["genres"]]) 

    return desc

def get_movie_image(id):
    url = BASE_URL + id + "/images"

    # create request
    r = requests.get(url, params={"api_key": KEY})

    # convert request to json
    r_json = r.json()
    #print(r_json["posters"][0])
    # find the first english language poster being searching through the list of dictionaries from the json
    poster = list(filter(lambda item: item["iso_639_1"] == "en", r_json["posters"]))[0]
    image = "https://image.tmdb.org/t/p/w500" + poster["file_path"]
    
    return image

print(get_movie(movie_id))
print(get_movie_image(movie_id))
