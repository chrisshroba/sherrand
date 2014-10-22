from flask import *
from random import randint
from mysql import get_db, teardown_db


app = Flask(__name__,
            static_folder="../static",
            static_path="")

# Turn off for production
app.debug = True


@app.route('/')
def root():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM sayings")
    sayings = list(cur.fetchall())
    return sayings[randint(0, len(sayings) - 1)]


@app.teardown_appcontext
def teardown(exception):
    teardown_db()
