from flask import *
from random import randint
from mysql import get_db, teardown_db
from jsonschema import validate, ValidationError
from RideRequest import RideRequest
from RideOffer import RideOffer
from Notification import Notification
from Matching import check_for_matches_offer, check_for_matches_request
import urllib2


app = Flask(__name__,
            static_folder="../static",
            static_path="")

# Turn off for production
app.debug = True

public_routes = []


def is_public(fn):
    public_routes.append(fn)
    return fn


def update_notifications():
    user = session["user"] if "user" in session else None
    if user:
        notifs = Notification.get_unread_by_user_id(user["id"])
        session["notifications"] = notifs
        session["has_unread"] = len(notifs) > 0

@app.route('/')
def root():
    if "user" in session:
        return redirect("/home")
    return redirect("/login")


@is_public
@app.route("/login", methods=["GET"])
def login_page():
    feedback = session["feedback"] if "feedback" in session else None
    feedback_code = session["feedback_code"] if "feedback_code" in session else None
    session["feedback"] = None
    session["feedback_code"] = None
    return render_template("login.html", simplenav='yes', feedback=feedback, feedback_code=feedback_code)


def lookup_user(username, password):
    db = get_db()
    cur = db.cursor()
    q = "SELECT * FROM Users WHERE username = %s AND password = PASSWORD(%s) LIMIT 1"
    cur.execute(q, (username, password))
    results = [dict(id=item[0], username=item[1], password=item[2], first_name=item[3], last_name=item[4], phone=item[5], email=item[6], score=item[7], photo=item[8], d_rating=item[9], p_rating=item[10]) for item in cur.fetchall()]
    if len(results) == 0:
        return None
    if results[0]["photo"] == None:
        results[0]["photo"] = "https://cdnil0.fiverrcdn.com/photos/419911/v2_680/img1.jpg"
    return results[0]

@is_public
@app.route("/api/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if (not username) or (not password):
        return jsonify({
            "user": None
        })

    user = lookup_user(username, password)
    
    session["user"] = user
    if user:
        return redirect("/home")
    else:
        print "here"
        session["feedback"] = "Invalid username or password"
        session["feedback_code"] = "warning"
        return redirect("/login")

@app.route("/logout")
def logout():
    session["user"] = None
    session["feedback"] = "Successfully logged out"
    session["feedback_code"] = "success"
    return redirect("/login")

@is_public
@app.route("/home", methods=["GET"])
def home_page():
    update_notifications()
    # session["events"] = lookup_events()
    # return str(lookup_events()[0][5])
    return render_template("home.html")

@is_public
@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html", simplenav='yes')

@is_public
@app.route("/api/signup", methods=["POST"])
def create_account():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    email = request.form.get("email")

    db = get_db()
    cur = db.cursor()
    q = """
        INSERT INTO Users (first_name, last_name, username, password, phone, email)
        VALUES (%s, %s, %s,PASSWORD(%s), %s, %s)
        """
    # print q
    res = cur.execute(q, (first_name, last_name, username, password, phone, email))
    db.commit()
    # print res
    
    session["feedback"] = "Account successfully created"
    session["feedback_code"] = "success"

    return redirect("/login")


def message_response(code, message):
    response = jsonify({"message": message})
    response.status_code = code
    return response

@app.route('/ride')
def ride_info():
    update_notifications()
    return render_template('ride_info.html')

@app.route('/profile')
def profile():
    update_notifications()
    return render_template('profile.html')

@app.route('/edit_profile')
def edit_profile_page():
    update_notifications()
    return render_template('edit_profile.html')

@app.route('/api/edit_profile', methods=['POST'])
def edit_profile():
    update_notifications()
    first_name = request.form.get("first_name") if "first_name" in request.form else session["user"]["first_name"]
    last_name = request.form.get("last_name") if "last_name" in request.form else session["user"]["last_name"]
    password = request.form.get("password") if "password" in request.form else session["user"]["passward"]
    phone = request.form.get("phone") if "phone" in request.form else session["user"]["phone"]
    email = request.form.get("email") if "email" in request.form else session["user"]["email"]

    db = get_db()
    cur = db.cursor()
    q = """
        UPDATE Users
            SET first_name = %s,
                last_name = %s,
                password = PASSWORD(%s), 
                phone = %s, 
                email = %s
        WHERE id = %s;
        """
    res = cur.execute(q, (first_name, last_name, password, phone, email, session["user"]["id"]))
    db.commit()

    user = lookup_user(session["user"]["username"], password)
    
    session["user"] = user
    
    session["feedback"] = "Account successfully created"
    session["feedback_code"] = "success"

    return redirect("/profile")

@app.route('/request')
def request_ride():
    update_notifications()
    return render_template('request_ride.html')


@app.route('/offer')
def offer_ride():
    update_notifications()
    return render_template('offer_ride.html')


@app.route('/api/requests', methods=['GET'])
def request_get_all():
    return jsonify({"request_list": RideRequest.get_all()})


@app.route('/api/requests/<int:request_id>', methods=['GET'])
def request_get_with_id(request_id):
    return jsonify(RideRequest.get_with_id(request_id))


@app.route('/api/requests/<int:request_id>', methods=['PUT'])
def request_update(request_id):
    j = request.get_json()
    try:
        validate(j, RideRequest.schema)
    except ValidationError as e:
        return message_response(400, "Malformed JSON request: " + e.message)
    new_request = RideRequest(j)
    new_request.id = request_id
    new_request.update()
    return message_response(200, "Successfully updated request!")


@app.route('/api/requests/<int:request_id>', methods=['DELETE'])
def request_delete(request_id):
    RideRequest.delete_with_id(request_id)
    return message_response(200, "Successfully deleted request!")


@app.route('/api/requests', methods=['POST'])
def request_add():
    req = RideRequest(
        {
            "user_id": session["user"]["id"],
            "title": "Ride Request",
            "start_date": request.form["date"],
            "end_date": request.form["date"],
            "start_time": request.form["start_time"],
            "end_time": request.form["end_time"],
            "origin": {
                "name": request.form["origin_name"],
                "lat": request.form["origin_lat"],
                "lng": request.form["origin_lon"]
            },
            "destination": {
                "name": request.form["dest_name"],
                "lat": request.form["dest_lat"],
                "lng": request.form["dest_lon"]
            }
        }
    )
    res = req.insert()
    return redirect("/request/" + str(res))


@app.route('/request/<int:request_id>')
def confirmation(request_id):
    ride = RideRequest.get_with_id(request_id)
    return render_template('request_info.html', ride=ride)


# @app.route('/api/offers', methods=['GET'])
# def offer_get_all():
#     return jsonify({"offer_list": RideOffer.get_all()})



@app.route('/offers/<int:offer_id>', methods=['GET'])
def offer_get_with_id(offer_id):
    offer = RideOffer.get_with_id(offer_id)
    return render_template('ride_info.html', offer=offer)


@app.route('/offers/<int:offer_id>', methods=['POST'])
def offer_get_with_id_post(offer_id):
    offer = RideOffer.get_with_id(offer_id)
    driver = offer["user_id"]
    requester = session["user"]["id"]

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT phone FROM Users WHERE id=%s", [driver])
    driver_phone = cur.fetchall()[0][0]
    cur = db.cursor()
    cur.execute("SELECT phone FROM Users WHERE id=%s", [requester])
    requester_phone = cur.fetchall()[0][0]

    url = "http://shroba.io:4555/setupProxy?num1=%s&num2=%s" % (requester_phone, driver_phone)
    make_proxy = urllib2.urlopen(url).open()

    return render_template('ride_info.html', offer=offer)


@app.route('/api/offers/<int:offer_id>', methods=['PUT'])
def offer_update(offer_id):
    j = request.get_json()
    try:
        validate(j, RideOffer.schema)
    except ValidationError as e:
        return message_response(400, "Malformed JSON request: " + e.message)
    new_offer = RideOffer(j)
    new_offer.id = offer_id
    new_offer.update()
    return message_response(200, "Successfully updated offer!")


@app.route('/api/offers/<int:offer_id>', methods=['DELETE'])
def offer_delete(offer_id):
    RideOffer.delete_with_id(offer_id)
    return message_response(200, "Successfully deleted offer!")


@app.route('/api/offers', methods=['POST'])
def offer_add():
    req = RideOffer(
        {
            "title": request.form["title"],
            "user_id": session["user"]["id"],
            "max_seats": request.form["max_seat"],
            "open_seats": request.form["max_seat"],
            "start_date": request.form["date"],
            "end_date": request.form["date"],
            "start_time": request.form["start_time"],
            "end_time": request.form["end_time"],
            "origin": {
                "name": request.form["origin_name"],
                "lat": request.form["origin_lat"],
                "lng": request.form["origin_lon"]
            },
            "destination": {
                "name": request.form["dest_name"],
                "lat": request.form["dest_lat"],
                "lng": request.form["dest_lon"]
            }
        }
    )
    res = req.insert()
    return redirect("/offers/" + str(res))

@app.before_request
def before_request():
    if request.endpoint and not session.get("user", None) and app.view_functions[request.endpoint] not in public_routes\
            and request.endpoint != "static":
        print "uh oh"
        print request.endpoint
        return redirect("/login")


def lookup_events():
    db = get_db()
    cur = db.cursor()
    q = "SELECT * FROM Offers "
    cur.execute(q)
    results = cur.fetchall()
    db.commit()

    if len(results) == 0:
        return None
    return results


@app.teardown_appcontext
def teardown(exception):
    teardown_db()

app.secret_key = '3be32335d4bCb0dCdE7BCACC5c41A8'

if __name__ == '__main__':  
    app.run()
