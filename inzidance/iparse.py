import requests
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
import time

URL = 'https://www.apps.nlga.niedersachsen.de/corona/iframe.php'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

trs = soup.find_all('tr')

leerTr = ""

for tr in trs:
    if "Leer" in str(tr):            
        leerTr = str(tr)
        break

leerSoup = BeautifulSoup(leerTr, 'html.parser')

inzTd = str(leerSoup.find_all('td')[4])

firstClosing = inzTd.find('>')
nextStarting = inzTd.find('<',firstClosing)

inzidenz = float((inzTd[firstClosing+1:nextStarting]).replace(',','.'))

client = InfluxDBClient(host='localhost', port=8086, username='user',password='pass', database='db')

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