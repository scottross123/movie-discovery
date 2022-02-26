import os
from dotenv import load_dotenv
from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
import random
import tmdb

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = os.getenv("SECRET_KEY")

class Users(db.Model):
    username = db.Column(db.String(30), primary_key=True, nullable=False)


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    movie_id = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(2000))


db.create_all()

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

    return flask.render_template(
        "index.html",
        title=movie[0],
        tagline=movie[1],
        genres=", ".join(movie[2]),
        poster=poster,
        url=url,
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        print(username)
        logged_in = Users.query.filter(Users.username == username).first()
        print(logged_in)
        if logged_in == None:
            print("user invalid")
            flask.flash("WRONG!")
            return flask.redirect(flask.url_for("login"))
        else:
            print("user verified")
            return flask.redirect(flask.url_for("index"))

    return flask.render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        print(username)
        query = Users.query.filter(Users.username == username).first()
        print(query)
        if query == None:
            flask.flash("New user created! Redirecting to login page...")
            print("user not in db, add user to db")
            db.session.add(Users(username = username))
            db.session.commit()
            return flask.redirect(flask.url_for("login"))
        else:
            print("user already in db")
            flask.flash("Hey! That user is already registered. Try again!")
            return flask.redirect(flask.url_for("signup"))

    return flask.render_template("signup.html")


@app.route("/save", methods=["POST"])
def form_handler():

    return flask.redirect("/")


# app is calm-atoll-21963 on heroku
app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)
