"""
Contains functions that interact witht TMDB and wikimedia API
"""

import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your API keys from .env

# api stuff
TMDB_KEY = os.getenv("TMDB_KEY")
TMDB_URL = "https://api.themoviedb.org/3/movie/"
MW_URL = "https://en.wikipedia.org/w/rest.php/v1/search/page"

def get_movie(id):
    url = TMDB_URL + id

    # create request
    r = requests.get(url, params={"api_key": TMDB_KEY})

    # convert request to json
    r_json = r.json()
    # for loop is used find collect the genres from the list of dictionaries returned by json
    desc = (r_json["title"], r_json["tagline"], [d["name"] for d in r_json["genres"]]) 

    return desc

def get_movie_image(id):
    url = TMDB_URL + id + "/images"

    # create request
    r = requests.get(url, params={"api_key": TMDB_KEY})

    # convert request to json
    r_json = r.json()
    #print(r_json["posters"][0])
    # find the first english language poster being searching through the list of dictionaries from the json
    poster = list(filter(lambda item: item["iso_639_1"] == "en", r_json["posters"]))[0]
    image = "https://image.tmdb.org/t/p/w500" + poster["file_path"]
    
    return image

def search_wiki(query):
    url = MW_URL
    # create request
    r = requests.get(url, params={"q": query + " (film)", "limit": 10})
    # convert request to json
    r_json = r.json()
    # return wikipedia url at the found id
    return "https://en.wikipedia.org/?curid=" + str(r_json["pages"][0]["id"])

