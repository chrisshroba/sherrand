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
    if request.endpoint and not session.get("user", None) and app.view_functions[request.endpoint] not in public_routes and request.endpoint!="static":
        print "uh oh"
        print request.endpoint
        return redirect("/login.html")



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
    return "Hi, I'm root"
@is_public
@app.route("/setSesh")
def ss():
    session["user"] = "foo"
    return "Done"

@is_public
@app.route("/deleteSesh")
def ds():
    session = {}
    return "Done"


def lookup_user(username, password):
    db = get_db()
    cur = db.cursor()
    q = "SELECT * FROM user WHERE username = '%s' AND pass = PASSWORD('%s') LIMIT 1" % (username, password)
    print q
    cur.execute(q)
    results = cur.fetchall()
    if len(results) == 0:
        return None
    return results[0]


@is_public
@app.route("/api/login", methods=["POST"])
def login():
    print "hi"
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if (not username) or (not password):
        return jsonify({
            "user": None
        })

    user = lookup_user(username, password)

    session["user"] = user
    if user:
        return redirect("/loginsuccess")
    else:
        return redirect("/login.html")

@app.route("/loginsuccess")
def loginsuccess():
    return "You have successful logged in."

@app.route("/logout")
def logout():
    session["user"] = None
    return "Logged out."

@is_public
@app.route("/createaccount", methods=["POST"])
def createaccount():
    print 1
    full_name = request.form.get("full_name")
    username = request.form.get("username")
    passwd = request.form.get("pass")
    phone = request.form.get("phone")
    email = request.form.get("email")
    print 2
    db = get_db()
    cur = db.cursor()
    print 3
    q = "INSERT INTO user (full_name, username, pass, phone, email) VALUES ('%s','%s',PASSWORD('%s'),'%s','%s')" % (full_name, username, passwd, phone, email)
    print q
    res = cur.execute(q)
    db.autocommit(True) #TODO move this to mysql.py?
    print res
    session["user"] = username
    print "sesh user was set"

    return "Created Account."



@app.teardown_appcontext
def teardown(exception):
    teardown_db()

app.secret_key = '3be32335d4bCb0dCdE7BcacC5c41A8'

#We'll turn off debug in production
app.debug=True
app.run(port=8000,host="0.0.0.0")
