from flask_login import LoginManager
from models import User

login = LoginManager()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))