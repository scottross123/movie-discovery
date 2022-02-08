"""
Contains functions that interact witht TMDB API
"""

import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your API keys from .env

URL = ""