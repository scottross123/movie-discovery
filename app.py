import os
from dotenv import load_dotenv
import flask
from dotenv import find_dotenv, load_dotenv
from flask_login import current_user, login_user, logout_user
from tmdb import get_movie, get_movie_image, search_wiki, pick_random_movie
from models import User, Rating, db, random_id
from auth import login

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

login.init_app(app)
db.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQL_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

choice = pick_random_movie()

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

@bp.route("/new_page")
def new_page():
    return flask.render_template("index.html")

@app.before_first_request
def create_all():
    db.create_all()

@app.route("/")
def home():
    return flask.render_template("login.html")

@app.route("/index")
def index():

    # error handling if something goes wrong with the apis
    try:
        movie = get_movie(choice)
    except:
        move = "Uh-oh, something went wrong, movie info can't be found"

    try:
        poster = get_movie_image(choice)
    except:
        poster = "/static/notfound.jpg"

    try:
        url = search_wiki(movie[0])
    except:
        url = "https://en.wikipedia.org/wiki/Lists_of_films"

    # list comments
    comments = Rating.query.filter(Rating.movie_id == choice).all()
    print(comments)

    return flask.render_template(
        "index.html",
        current_user=current_user.username,
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
            login_user(user)
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
    logout_user()
    return flask.redirect(flask.url_for("login"))

@app.route("/save", methods=["POST", "GET"])
def add_comment():
    if flask.request.method == "POST":
        data = flask.request.form
        new_comment = Rating(
            rating_id = random_id(),
            username = current_user.username, # user currently logged in
            movie_id = choice, # movie id
            rating = data["rating"],
            content = data["content"]           
        )
        db.session.add(new_comment)
        db.session.commit()
    return flask.redirect(flask.url_for("index"))

@app.route("/save_edits", methods=["POST", "GET"])
def edit_comment():
    if flask.request.method == "POST":
        user_ratings = Rating.query.filter_by().all()
        data = flask.request.form
        new_comments = [Rating(
            rating_id = random_id(),
            username = current_user.username, # user currently logged in
            movie_id = choice, # movie id
            rating = data["rating"],
            content = data["content"]           
        )
        for comment in data]

    # delete old ratings
    for rating in user_ratings:
        db.session.delete(rating)

    # add new ratings
    for rating in new_comments:
        db.session.add(rating)
    
    db.session.commit()

    return flask.jsonify("New ratings saved!!")

@app.route("/get_reviews")
def foo():
    ratings = Rating.query.filter().all()
    print(ratings)
    return flask.jsonify(
        [
            {
                "username": rating.username,
                "movie_id": rating.movie_id,
                "rating": rating.rating,
                "content": rating.content
            }
            for rating in ratings
        ]
    )


app.register_blueprint(bp)

# app is calm-atoll-21963 on heroku
app.run(port=5000, debug=True)
