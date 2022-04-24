import joblib
import numpy as np
import sqlite3
import requests
from flask import g
TRUNCATE_SIZE = 1000
DATABASE = './schemas/syslog.db'
def get_db():
    db = getattr(g, '_database', None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def train_model(filename):
    #read untrained model from saved_models
    model = joblib.load("saved_models/" + filename)
    # train the model
    model = train(model)
    # save the model to trained_models
    joblib.dump(model, filename)
    # set the model status to 1 in sqlite
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        f"INSERT INTO models (model_name, isactive) VALUES('{filename.split('.')[0]}', 1)"
    )
    conn.commit()
    conn.close()

def train(model):
    X_train = np.load('data/X_train.npy')[:TRUNCATE_SIZE]
    y_train = np.load('data/y_train.npy')[:TRUNCATE_SIZE]
    X_test = np.load('data/X_test.npy')
    y_test = np.load('data/y_test.npy')
    print("training the new mode...")
    model = model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(score)
    return model

def get_geo(ip):
    try:
        api = f"https://apis.map.qq.com/ws/location/v1/ip?output=json&key=KUQBZ-FYDCU-YMVVN-2DDW5-7WDYE-5JBJR&ip={ip}"
        r = requests.get(api)
        r = r.json()
        print(r)
        return (r['result']['location']['lng'], r['result']['location']['lat'])
    except:
        return None, None

def get_model(name):
    conn = sqlite3.connect(DATABASE)
    res = conn.execute(f"""
    SELECT id, model_name FROM models WHERE lower(model_name) = '{name}'
    """).fetchall()
    if res:
        return res[0][0]
    else:
        return None