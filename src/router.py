from flask import *
from mysql import get_db, teardown_db
from random import randint


app = Flask(__name__,
            static_folder="../static",
            static_path="")

public_routes = []


def is_public(fn):
    public_routes.append(fn)
    return fn


@app.before_request
def before_request():
    if request.endpoint and not session.get("user", None) and app.view_functions[request.endpoint] not in public_routes\
            and request.endpoint != "static":
        print "uh oh"
        print request.endpoint
        return redirect("/login")


@app.route('/')
def root():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM sayings")
    sayings = list(cur.fetchall())
    return sayings[randint(0, len(sayings) - 1)]


def lookup_user(username, password):
    db = get_db()
    cur = db.cursor()
    q = "SELECT * FROM Users WHERE username = %s AND pass = PASSWORD(%s) LIMIT 1"
    print q
    cur.execute(q, (username, password))
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
        return redirect("/login")

@is_public
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/loginsuccess")
def login_success():
    return "You have successful logged in."


@app.route("/logout")
def logout():
    session["user"] = None
    return "Logged out."


@is_public
@app.route("/createaccount", methods=["POST"])
def create_account():
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
    q = """
        INSERT INTO Users (full_name, username, pass, phone, email)
        VALUES (%s, %s,PASSWORD(%s), %s, %s)
        """
    print q
    res = cur.execute(q, (full_name, username, passwd, phone, email))
    db.commit()
    print res
    session["user"] = username
    print "sesh user was set"

    return "Created Account."


@is_public
@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.teardown_appcontext
def teardown(exception):
    teardown_db()

app.secret_key = '3be32335d4bCb0dCdE7BCACC5c41A8'

#We'll turn off debug in production
app.debug = True
