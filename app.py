import random
import flask
import tmdb
import os

app = flask.Flask(__name__)

# movie ids for Dune, Encanto, and Spider-Man: No Way Home
movies = ["438631", "568124", "634649"]


@app.route("/")
def index():
    choice = random.choice(movies)

    # error handling if something goes wrong with the apis
    try:
        movie = tmdb.get_movie(choice)
    except:
        move = "Uh-oh, something went wrong, movie info can't be found"
    
    try:
        poster = tmdb.get_movie_image(choice)
    except:
        poster = "/static/notfound.jpg"

    try:
        url = tmdb.search_wiki(movie[0])
    except:
        url = "https://en.wikipedia.org/wiki/Lists_of_films"

    return flask.render_template("index.html", 
        title=movie[0], 
        tagline=movie[1], 
        genres=", ".join(movie[2]),
        poster=poster,
        url=url
    )

# app is calm-atoll-21963 on heroku 
app.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),
    debug=True
)