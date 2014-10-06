__author__ = 'chrisshroba'

from flask import *

app = Flask(__name__,
            static_folder="../static",
            static_path="")


@app.route('/')
def root():
    return app.send_static_file('index.html')



app.run(port=80,host="0.0.0.0",debug =True) #We'll turn off debug in production