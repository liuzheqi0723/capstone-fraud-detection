from flask import Flask
from flask import g
import sqlite3
from flask import Flask, flash, request, redirect, url_for
import os
from flask_cors import CORS, cross_origin

DATABASE = './schemas/syslog.db'
UPLOAD_FOLDER = './saved_models'
ALLOWED_EXTENSIONS = {'joblib'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    db = getattr(g, '_database', None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins=['*'])

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/ping")
def ping():
    return "pong"

@app.route('/models', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "File not Found"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db()
        #
        cmd = f"INSERT INTO models (modelname) VALUES('{filename.split('.')[0]}')"
        print(cmd)
        conn.execute(cmd)
        conn.commit()
    return "OK"

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)