__author__ = 'chrisshroba'

from flask import *
from flask_login import *

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def root():
    return "This is root!"

class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

chris = User(1, "Christopher")
alexandra = User(2, "Alexandra")
users = {
    chris.id: chris,
    alexandra.id: alexandra
}
@login_manager.user_loader
def load_user(userid):
    return users.get(userid)


app.run(port =7799, debug = True)