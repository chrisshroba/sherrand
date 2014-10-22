import string
from flask import *
from random import randint
from mysql import get_db, teardown_db
import random
import MySQLdb
from flask_login import *


app = Flask(__name__,
            static_folder="../sherrand",
            static_path="")

public_routes=[]
def is_public(fn):
    public_routes.append(fn)
    return fn



@app.before_request
def before_request():
    if not session.get("user", None) and request.endpoint not in public_routes:
        redirect(url_for(login))




@app.route('/')
def root():
    # db = MySQLdb.connect(host="localhost",
    #                      user="root",
    #                      passwd="",
    #                      db="test")
    # cur = db.cursor()
    # cur.execute("SELECT * FROM sayings")
    # sayings = list(cur.fetchall())
    # db.close()
    return "Hi"

@app.route("/setSesh")
def ss():
    session["user"] = "foo"
    return "Done"

@app.teardown_appcontext
def teardown(exception):
    teardown_db()
@app.route("/api/login", methods=["POST"])
def login():
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if (not username) or (not password):
        return jsonify({
            "user": None
        })

    session["user"] = username



app.secret_key = ''.join(random.choice(string.hexdigits) for n in xrange(30))
app.run(port=80,host="0.0.0.0",debug =True) #We'll turn off debug in production