from flask import *
from random import randint
import MySQLdb


app = Flask(__name__,
            static_folder="../static",
            static_path="")

# Turn off for production
app.debug = True


@app.route('/')
def root():
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="password",
                         db="test")
    cur = db.cursor()
    cur.execute("SELECT * FROM sayings")
    sayings = list(cur.fetchall())
    db.close()
    return sayings[randint(0, len(sayings) - 1)]



#app.run(debug =True) #We'll turn off debug in production