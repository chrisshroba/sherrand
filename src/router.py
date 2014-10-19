from flask import *
from random import randint
import MySQLdb


app = Flask(__name__,
            static_folder="../static",
            static_path="")

# Turn off for production
app.debug = True


def connect_to_database():
    return MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="password",
                           db="test")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@app.route('/')
def root():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM sayings")
    sayings = list(cur.fetchall())
    return sayings[randint(0, len(sayings) - 1)]


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        g._database = None