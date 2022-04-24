from pyexpat import model
from flask import g
from flask import Flask, flash, request, redirect, url_for
import os
from flask_cors import CORS, cross_origin
from datetime import datetime
import numpy as np
import joblib
import json
from urllib.request import parse_http_list
import pandas as pd
from utils import train_model, get_db, get_geo, get_model
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from faker import Faker

#macros
UPLOAD_FOLDER = './saved_models'
ALLOWED_EXTENSIONS = {'joblib'}
COLUMNS = ['id_01', 'id_02', 'id_05', 'id_06', 'id_11', 'id_12', 'id_13', 'id_15', 'id_16', 'id_17', 'id_19', 'id_20', 'id_28', 'id_29', 'id_31', 'id_35', 'id_36', 'id_37', 'id_38', 'DeviceType', 'DeviceInfo', 'TransactionDT', 'TransactionAmt', 'ProductCD', 'card1', 'card2', 'card3', 'card4', 'card5', 'card6', 'addr1', 'addr2', 'P_emaildomain', 'R_emaildomain', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D12', 'D13', 'D14', 'D15', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'V29', 'V30', 'V31', 'V32', 'V33', 'V34', 'V35', 'V36', 'V37', 'V38', 'V39', 'V40', 'V41', 'V42', 'V43', 'V44', 'V45', 'V46', 'V47', 'V48', 'V49', 'V50', 'V51', 'V52', 'V53', 'V54', 'V55', 'V56', 'V57', 'V58', 'V59', 'V60', 'V61', 'V62', 'V63', 'V64', 'V65', 'V66', 'V67', 'V68', 'V69', 'V70', 'V71', 'V72', 'V73', 'V74', 'V75', 'V76', 'V77', 'V78', 'V79', 'V80', 'V81', 'V82', 'V83', 'V84', 'V85', 'V86', 'V87', 'V88', 'V89', 'V90', 'V91', 'V92', 'V93', 'V94', 'V95', 'V96', 'V97', 'V98', 'V99', 'V100', 'V101', 'V102', 'V103', 'V104', 'V105', 'V106', 'V107', 'V108', 'V109', 'V110', 'V111', 'V112', 'V113', 'V114', 'V115', 'V116', 'V117', 'V118', 'V119', 'V120', 'V121', 'V122', 'V123', 'V124', 'V125', 'V126', 'V127', 'V128', 'V129', 'V130', 'V131', 'V132', 'V133', 'V134', 'V135', 'V136', 'V137', 'V138', 'V139', 'V140', 'V141', 'V142', 'V143', 'V144', 'V145', 'V146', 'V147', 'V148', 'V149', 'V150', 'V151', 'V152', 'V153', 'V154', 'V155', 'V156', 'V157', 'V158', 'V159', 'V160', 'V161', 'V162', 'V163', 'V164', 'V165', 'V166', 'V167', 'V168', 'V169', 'V170', 'V171', 'V172', 'V173', 'V174', 'V175', 'V176', 'V177', 'V178', 'V179', 'V180', 'V181', 'V182', 'V183', 'V184', 'V185', 'V186', 'V187', 'V188', 'V189', 'V190', 'V191', 'V192', 'V193', 'V194', 'V195', 'V196', 'V197', 'V198', 'V199', 'V200', 'V201', 'V202', 'V203', 'V204', 'V205', 'V206', 'V207', 'V208', 'V209', 'V210', 'V211', 'V212', 'V213', 'V214', 'V215', 'V216', 'V217', 'V218', 'V219', 'V220', 'V221', 'V222', 'V223', 'V224', 'V225', 'V226', 'V227', 'V228', 'V229', 'V230', 'V231', 'V232', 'V233', 'V234', 'V235', 'V236', 'V237', 'V238', 'V239', 'V240', 'V241', 'V242', 'V243', 'V244', 'V245', 'V246', 'V247', 'V248', 'V249', 'V250', 'V251', 'V252', 'V253', 'V254', 'V255', 'V256', 'V257', 'V258', 'V259', 'V260', 'V261', 'V262', 'V263', 'V264', 'V265', 'V266', 'V267', 'V268', 'V269', 'V270', 'V271', 'V272', 'V273', 'V274', 'V275', 'V276', 'V277', 'V278', 'V279', 'V280', 'V281', 'V282', 'V283', 'V284', 'V285', 'V286', 'V287', 'V288', 'V289', 'V290', 'V291', 'V292', 'V293', 'V294', 'V295', 'V296', 'V297', 'V298', 'V299', 'V300', 'V301', 'V302', 'V303', 'V304', 'V305', 'V306', 'V307', 'V308', 'V309', 'V310', 'V311', 'V312', 'V313', 'V314', 'V315', 'V316', 'V317', 'V318', 'V319', 'V320', 'V321', 'V322', 'V323', 'V324', 'V325', 'V326', 'V327', 'V328', 'V329', 'V330', 'V331', 'V332', 'V333', 'V334', 'V335', 'V336', 'V337', 'V338', 'V339']

# global variables
users_geo_centroid = []
models = {}
nan_processor = None

# filter out files that not allowed to upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Cross Origin setup
CORS(app, origins=['*'])

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/ping")
def ping():
    print(request.environ.get('REMOTE_ADDR'))
    return {"msg": "pong"}

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
        cmd = f"INSERT INTO models (modelname) VALUES('{filename.split('.')[0]}')"
        train_model(filename)
        conn.execute(cmd)
        conn.commit()
        conn.close()
    return "OK"

@app.route('/search_model', methods=['GET'])
def search_model():
    ip = request.remote_addr
    if ip == '127.0.0.1' or ip == '0':
        ex = Faker()
        ip = ex.ipv4()
    long, lat = get_geo(ip)
    args = request.args.to_dict()
    res = {}
    conn = get_db()
    if args.get('model', None):
        model_id = get_model(args.get('model'))
        if model_id:
            res['result'] = conn.execute(
            f"""SELECT count(*), m.model_name, pred.result 
            FROM prediction_log pred 
            LEFT JOIN models m 
            ON pred.model_id = m.id 
            WHERE m.isactive = 1 and m.id = {model_id}
            GROUP BY m.model_name, pred.result"""
        ).fetchall()
    else:
        res['result'] = conn.execute(
            f"""SELECT count(*), m.model_name, pred.result 
            FROM prediction_log pred 
            LEFT JOIN models m 
            ON pred.model_id = m.id 
            WHERE m.isactive = 1
            GROUP BY m.model_name, pred.result"""
        ).fetchall()
    if long and lat:
        cmd = f"""
            INSERT INTO view_log (ip, long, lat, viewtime) VALUES('{ip}', {long}, {lat}, CURRENT_TIMESTAMP)
        """
    else:
        cmd = f"""
            INSERT INTO view_log (ip, viewtime) VALUES('{ip}', CURRENT_TIMESTAMP)
        """

    print(cmd)
    conn.execute(cmd)
    conn.commit()
    conn.close()
    return res

@app.route('/server_time', methods=['GET'])
def server_time():
    global start_time
    return {"server_time": (datetime.now() - start_time).total_seconds()}

@app.route('/summary', methods=["GET"])
def summary():
    conn = get_db()
    fraud_cnt = conn.execute(
        "SELECT count(*) FROM prediction_log WHERE result=0"
        ).fetchone()[0]
    auth_cnt = conn.execute(
        "SELECT count(*) FROM prediction_log WHERE result=1"
        ).fetchone()[0]
    print(type(auth_cnt), auth_cnt)
    return {
        "fraud_cnt":fraud_cnt,
        "auth_cnt":auth_cnt
    }
@app.route('/usersgeo', methods=['GET'])
def usersgeo():
    conn = get_db()
    geos = conn.execute("""
        SELECT long, lat FROM view_log WHERE long is not NULL and lat is not NULL ORDER BY RANDOM() LIMIT 100
    """).fetchall()
    return {"result":geos}

@app.route('/prediction', methods =['GET'])
def predict():
    ip = request.remote_addr
    if ip == '127.0.0.1' or ip == '0':
        ex = Faker()
        ip = ex.ipv4()
        print(ip)
    long, lat = get_geo(ip)
    args = request.args.to_dict()
    if len(request.json["data"]) != 410:
        return {"ERROR": "INPUT DIMENSION IS INCORECT, INPUT SHOULD HAVE 410 columns"}
    model_name = args.get('model')
    res = {}
    data = np.array(request.json["data"]).astype(np.float).reshape(1, -1)
    data = pd.DataFrame(data, columns=COLUMNS)
    data = nan_processor.transform(data)
    if model_name:
        start_time = datetime.now()
        res[model_name] = models[str.lower(model_name)].predict(data).tolist()[0]
        seconds = (datetime.now() - start_time).microseconds
        model_id = get_model(model_name)
        conn = get_db()
        if long and lat:
            print(f"""
            INSERT INTO prediction_log (model_id, result, input, ip, long, lat, responsetime) 
            VALUES ({model_id}, {res[model_name]}, '{str(data)}', '{ip}', {long}, {lat}, {seconds})
            """)
            conn.execute(f"""
            INSERT INTO prediction_log (model_id, result, input, ip, long, lat, responsetime) 
            VALUES ({model_id}, {res[model_name]}, '{str(data)}', '{ip}', {long}, {lat}, {seconds})
            """)
        else:
            print(f"""
            INSERT INTO prediction_log (model_id, result, input, responsetime) 
            VALUES ({model_id}, {res[model_name]}, '{str(data)}', {seconds})
            """)
            conn.execute(f"""
            INSERT INTO prediction_log (model_id, result, input, responsetime) 
            VALUES ({model_id}, {res[model_name]}, '{str(data)}', {seconds})
            """)
        conn.commit()
        conn.close()
    else:
        conn = get_db()
        for model in models:
            start_time = datetime.now()
            res[model] = models[model].predict(data).tolist()[0]
            seconds = (datetime.now() - start_time).microseconds
            model_id = get_model(model)
            if long and lat:
                print(f"""
                INSERT INTO prediction_log (model_id, result, input, ip, long, lat, responsetime) 
                VALUES ({model_id}, {res[model]}, '{str(data)}', '{ip}', {long}, {lat}, {seconds})
                """)
                conn.execute(f"""
                INSERT INTO prediction_log (model_id, result, input, ip, long, lat, responsetime) 
                VALUES ({model_id}, {res[model]}, '{str(data)}', '{ip}', {long}, {lat}, {seconds})
                """)
            else:
                print(f"""
                INSERT INTO prediction_log (model_id, result, input, responsetime) 
                VALUES ({model_id}, {res[model]}, '{str(data)}', {seconds})
                """)
                conn.execute(f"""
                INSERT INTO prediction_log (model_id, result, input, responsetime) 
                VALUES ({model_id}, {res[model]}, '{str(data)}', {seconds})
                """)
            conn.commit()
        conn.close()
    # save the log to sqlite
    
    print(res)
    return json.dumps(res)

def load_models():
    global models, nan_processor
    for filename in os.listdir('./trained_models'):
        if filename == 'nan_processor.joblib':
            continue
        if filename.rsplit('.', 1)[-1] == 'joblib':
            models[str.lower(filename.split('.')[0])] = joblib.load('./trained_models/' + filename)
        else:
            clf = xgb.XGBClassifier()
            booster = xgb.Booster()
            booster.load_model('./trained_models/' + filename)
            clf._Booster = booster
            clf._le = LabelEncoder().fit([1, 0])
            models[str.lower(filename.split('.')[0])] =clf
    nan_processor = joblib.load('./trained_models/nan_processor.joblib')

if __name__ == "__main__":
    global start_time
    start_time = datetime.now()
    app.secret_key = os.urandom(24)
    load_models()
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
    
