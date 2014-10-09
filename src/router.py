from flask import *
from random import randint
import MySQLdb


app = Flask(__name__,
            static_folder="../static",
            static_path="")


@app.route('/')
def root():
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="test")
    cur = db.cursor()
    cur.execute("SELECT * FROM sayings")
    sayings = list(cur.fetchall())
    db.close()
    return sayings[randint(0, len(sayings) - 1)]



app.run(port=80,host="0.0.0.0",debug =True) #We'll turn off debug in production