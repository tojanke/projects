import requests
import json
from influxdb import InfluxDBClient
import time

URL = 'https://api.corona-zahlen.org/districts/03457/'
resp = requests.get(URL)

if(resp.ok):
    jData = json.loads(resp.content)
    inzidenz = jData['data']['03457']['weekIncidence']
    client = InfluxDBClient(host='', port=, username='',password='', database='')

    json_body = [
        {
            "measurement": "inzidenzLeer",        
            "time": int(time.time() * 1000000000),
            "fields": {            
                "inzidenz": inzidenz
            }
        }
    ]
    client.write_points(json_body)
