import os
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE="flaskr"
))

def connect_db():
    "Abre una conexion con la BBDD."
    client = MongoClient()
    return {"db": client[app.config['DATABASE']], "client": client}

# Flask provides two contexts: the application context and the request context
# the request variable is the request object associated with the current request, whereas g is a general purpose variable associated with the current application context
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g,"mongo_db"):
        conn = connect_db()
        g.mongo_db = conn["db"]
        g.mongo_client = conn["client"]
    return g.mongo_db

# Registers a function to be called when the application context ends. 
# These functions are typically also called when the request context is popped
# the app context is created before the request comes in and is destroyed (torn down) whenever the request finishes
@app.teardown_appcontext
def close_db(error):
    "Cierra la BBDD"
    if error : 
        print(error)
        return
    if hasattr(g, "mongo_db"):
        g.mongo_client.close()
