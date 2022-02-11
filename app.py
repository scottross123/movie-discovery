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
    movie = tmdb.get_movie(choice)
    poster = tmdb.get_movie_image(choice)
    url = tmdb.search_wiki(movie[0])

    return flask.render_template("index.html", 
        title=movie[0], 
        tagline=movie[1], 
        genres=", ".join(movie[2]),
        poster=poster,
        url=url
    )
    
app.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),
    debug=True
)