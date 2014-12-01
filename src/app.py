from flask import *
from random import randint
from mysql import get_db, teardown_db
from jsonschema import validate, ValidationError
from RideRequest import RideRequest
from RideOffer import RideOffer

app = Flask(__name__,
            static_folder="../static",
            static_path="")

# Turn off for production
app.debug = True


def message_response(code, message):
    response = jsonify({"message": message})
    response.status_code = code
    return response


@app.route('/')
def root():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM sayings")
    sayings = list(cur.fetchall())
    return sayings[randint(0, len(sayings) - 1)]


@app.route('/request')
def request_ride():
    return render_template('request_ride.html')


@app.route('/offer')
def offer_ride():
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
    j = request.get_json()
    try:
        validate(j, RideRequest.schema)
    except ValidationError as e:
        return message_response(400, "Malformed JSON request: " + e.message)
    new_request = RideRequest(j)
    new_request.insert()
    return message_response(200, "Successfully added request!")


@app.route('/api/offers', methods=['GET'])
def offer_get_all():
    return jsonify({"offer_list": RideOffer.get_all()})


@app.route('/api/offers/<int:offer_id>', methods=['GET'])
def offer_get_with_id(offer_id):
    return jsonify(RideOffer.get_with_id(offer_id))


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
    j = request.get_json()
    try:
        validate(j, RideOffer.schema)
    except ValidationError as e:
        return message_response(400, "Malformed JSON request: " + e.message)
    new_offer = RideOffer(j)
    new_offer.insert()
    return message_response(200, "Successfully added offer!")



@app.teardown_appcontext
def teardown(exception):
    teardown_db()
