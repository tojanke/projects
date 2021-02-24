import io
import time
import base64
import mysql.connector
import requests

nextUpload = time.time()
uploadFrequency = 30

mydb = mysql.connector.connect(host="localhost", user="service", password="storch",database='storch')
mycursor = mydb.cursor()

def doUpload():

    global uploadFrequency, nextUpload

    mycursor.execute("SELECT thumbs.id, thumbs.thumb, pictures.timestamp FROM thumbs JOIN pictures ON thumbs.pictureid = pictures.id WHERE online = 0")

    newthumbs = mycursor.fetchall()    

    for thumb in newthumbs:
        url = "https://storch.tojanke.de/uploadimage.php"
        data = {"frameid": thumb[0], "thumbnail" : thumb[1], "timestamp": thumb[2]}
        if requests.post(url, data).status_code == requests.codes.ok :                    
            sql = "UPDATE thumbs SET online = 1 WHERE id = (%s)"    
            sqlvalues = (thumb[0],)    
            mycursor.execute(sql, sqlvalues)
            mydb.commit()

    nextUpload = nextUpload + uploadFrequency

if __name__ == "__main__":
    while(True):
        timeNow = time.time()
        if(timeNow >= nextUpload):
            doUpload()        
        time.sleep(1)
