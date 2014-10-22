from flask import g
import MySQLdb


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


def teardown_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        g._database = None
