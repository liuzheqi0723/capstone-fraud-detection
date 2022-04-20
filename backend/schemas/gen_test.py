import numpy as np
import random
from datetime import datetime, timedelta
from faker import Faker
import requests
import time
# returns (lat, lon)
def randlatlon():
    return (round(random.uniform( -90,  90), 5),
            round(random.uniform(-180, 180), 5))

def get_geo(ip):
    api = f"https://apis.map.qq.com/ws/location/v1/ip?output=json&key=KUQBZ-FYDCU-YMVVN-2DDW5-7WDYE-5JBJR&ip={ip}"
    r = requests.get(api)
    r = r.json()
    return (r['result']['location']['lng'], r['result']['location']['lat'])

with open("./sample_data.schema", "a") as f:
    for i in range(100):
        print(i)
        ex = Faker()
        ip = ex.ipv4()
        try:
            long, lat = get_geo(ip)
        except:
            continue
        service_id = i
        lat, long = randlatlon()
        f.write(f"""
        INSERT INTO prediction_log(model_id, result, input, ip, long, lat, responsetime) VALUES({np.random.choice([1, 2, 3])}, {np.random.choice([0, 1], p=[0.8, 0.2])}, 'test', '{ip}', {long}, {lat}, {700});
        """)
        time.sleep(3)