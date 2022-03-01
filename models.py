from flask_sqlalchemy import SQLAlchemy
import flask_login as fl
import random

db = SQLAlchemy()

class User(fl.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    movie_id = db.Column(db.String(30))
    rating = db.Column(db.Integer)
    content = db.Column(db.String(2000))

def random_id():
    min = 100
    max = 1000000000
    rand = random.randint(min, max)

    while Rating.query.filter(Rating.rating_id == rand).limit(1).first() and User.query.filter(User.id == rand).limit(1).first() is not None:
        rand = random.randint(min, max)


    return rand