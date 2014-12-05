__author__ = 'chrisshroba'
from twilio.rest import TwilioRestClient
from random import randint
from flask import *
# put your own credentials here
ACCOUNT_SID = "ACd368686e043e3cf0d06b1b788e53c41f"
AUTH_TOKEN = "7fcf3d1b071edad2da0427d10a79a85d"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

numbers = [u"+17083156123",
           u"+17082189191",
           u"+17082189074"]

chris = u"+17087901775"
alexandra = u"+17082050995"
serin=u"+12017835047"
marie=u"+16306961372"


number_maps = {}
for number in numbers:
    number_maps[number] = {}



def get_random_number():
    return numbers[randint(0, len(numbers)-1)]

def setup_number_proxy(num1, num2):
    num1 = num1.replace("-", "")
    num2 = num2.replace("-", "")

    ret_num = None
    for number in numbers:
        if num1 not in number_maps[number] and num2 not in number_maps[number]:
            number_maps[number][num1] = num2
            number_maps[number][num2] = num1
            ret_num = number
            break
    return ret_num


#print "Number: %s" % setup_number_proxy(chris, alexandra)
#print "Number: %s" % setup_number_proxy(chris,     serin)

## TEST SETUP
# print "Chris and Marie: %s" % setup_number_proxy(chris, marie)
# print "Chris and Chris: %s" % setup_number_proxy(chris, chris)
# print "Chris and Alexandra: %s" % setup_number_proxy(chris, alexandra)
# print "Chris and serin: %s" % setup_number_proxy(chris, serin)




app = Flask(__name__)

@app.route("/twilio/newMessage", methods=["POST"])
def new_message():
    from_number = request.form.get("From", None)
    to_twilio_number = request.form.get("To", None)
    body = request.form.get("Body", "Error")

    if from_number is None:
        return "from_number is None"
    if to_twilio_number is None:
        return "to_twilio_number is None"

    recipient_number = number_maps[to_twilio_number].get(from_number, None)

    if recipient_number is None:
        client.messages.create(
            to=from_number,
            from_=to_twilio_number,
            body="This number has not been set up for forwarding with Sherrand.",
        )
        return "Pair not found in map: %s" % ((from_number, to_twilio_number),)

    client.messages.create(
        to=recipient_number,
        from_=to_twilio_number,
        body=body,
    )

    return "Success"



@app.route("/setupProxy")
def setupProxyRoute():
    num1 = request.args.get("num1")
    num2 = request.args.get("num2")
    if num1[0]=="1":
        num1="+"+num1
    else:
        num1="+1"+num1

    if num2[0]=="1":
        num2="+"+num2
    else:
        num2="+1"+num2


    ret = setup_number_proxy(num1, num2)
    if ret is not None:
        client.messages.create(
            to=num1,
            from_=ret,
            body="Reply to this message to chat!",
            )
        return "Successful"

    return"Failed"

@app.route("/reset")
def resetRoute():
    global number_maps
    number_maps = {}
    for number in numbers:
        number_maps[number] = {}
    return "Done resetting."

app.run(host="0.0.0.0", debug=True, port=4555)



