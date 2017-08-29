import os
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE="flaskr",
    USERNAME="root",
    PASSWORD="root"
))

def connect_db():
    "Abre una conexion con la BBDD."
    client = MongoClient()
    # retorno un mapa con acceso a la bbdd y al cliente para manipular el cierre de sesion luego
    return {"db": client[app.config['DATABASE']], "client": client}

# Flask provides two contexts: the application context and the request context
# the request variable is the request object associated with the current request, whereas g is a general purpose variable associated with the current application context
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    # hasattr verifica la existencia de un atributo en un diccionario
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

def init_db():
    "Inicializa la BBDD"
    get_db()


# The app.cli.command() decorator registers a new command with the flask script. When the command executes,
# Flask will automatically create an application context which is bound to the right application. Within the function,
# you can then access flask.g and other things as you might expect
@app.cli.command('initdb')
def initdb_command():
    "Llama a la inicializacion de la BBDD"
    init_db()
    print("BBDD inicializada")

@app.route('/')
def show_entries():
    """Busca las entradas en la BBDD y luego renderiza una vista
    mostrando las entradas halladas"""
    db = get_db()
    coll = db.entries
    entries = coll.find()
    arr_entries = []
    for entry in entries:
        arr_entries.append(entry)
    return render_template('show_entries.html', entries=arr_entries)

@app.route('/add', methods=['POST'])
def add_entry():
    """Permite agregar una entrada"""
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    entry = {"title": request.form['title'], "text": request.form['text']}
    coll = db.entries
    entry_id = coll.insert_one(entry).inserted_id
    print(entry_id)
    flash("New entry was posted!")
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
    """Permite obtener el formulario de inicio de sesion y
    subir un formulario completado para iniciar sesion"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Cierra sesion de un usuario"""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
