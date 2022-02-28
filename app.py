import os
from dotenv import load_dotenv
from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
import random
import tmdb
import flask_login as fl

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

login_manager = fl.LoginManager()
login_manager.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = os.getenv("SECRET_KEY")

class User(fl.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    movie_id = db.Column(db.String(30))
    rating = db.Column(db.Integer)
    content = db.Column(db.String(2000))


db.create_all()

# movie ids for Dune, Encanto, and Spider-Man: No Way Home
movies = ["438631", "568124", "634649"]
choice = random.choice(movies)

def random_id():
    min = 100
    max = 1000000000
    rand = random.randint(min, max)

    while Rating.query.filter(Rating.rating_id == rand).limit(1).first() and User.query.filter(User.id == rand).limit(1).first() is not None:
        rand = random.randint(min, max)


    return rand

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def home():
    return flask.render_template("login.html")

@app.route("/index")
def index():

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

    # list comments
    comments = Rating.query.filter(Rating.movie_id == choice).all()
    print(comments)

    return flask.render_template(
        "index.html",
        current_user=fl.current_user.username,
        title=movie[0],
        tagline=movie[1],
        genres=", ".join(movie[2]),
        poster=poster,
        url=url,
        comments=comments
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        print(username)
        user = User.query.filter_by(username=username).first()
        print(user)
        flask.session.pop('_flashes', None)
        if user == None:
            print("user invalid")
            flask.flash("WRONG! User invalid!")
        else:
            print("user verified")
            fl.login_user(user)
            return flask.redirect(flask.url_for("index"))

    return flask.render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        print(username)
        query = User.query.filter(User.username == username).first()
        print(query)
        flask.session.pop('_flashes', None)
        if query == None:
            print("user not in db, add user to db")
            new_user = User(
                id = random_id(),
                username = username) 
            db.session.add(new_user)
            db.session.commit()
            return flask.redirect(flask.url_for("login"))
        else:
            print("user already in db")
            flask.flash("Hey! That user is already registered. Try again!")
            return flask.redirect(flask.url_for("signup"))

    return flask.render_template("signup.html")

@app.route("/logout")
def logout():
    fl.logout_user()
    return flask.redirect(flask.url_for("login"))

@app.route("/save", methods=["POST", "GET"])
def add_comment():
    if flask.request.method == "POST":
        data = flask.request.form
        new_comment = Rating(
            rating_id = random_id(),
            username = flask.session["username"], # user currently logged in
            movie_id = choice, # movie id
            rating = data["rating"],
            content = data["content"]           
        )
        db.session.add(new_comment)
        db.session.commit()
    return flask.redirect(flask.url_for("index"))


# app is calm-atoll-21963 on heroku
app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)
