import io
import time
import picamera
import base64
import mysql.connector
from PIL import Image
from timeloop import Timeloop
from datetime import timedelta

nextPictureTime = 0
nextConfUpdate = 0
pictureCounter = 0
pictureQuality = 50
thumbFrequency = 15
timelapseFrequency = 60
configFrequency = 300

mydb = mysql.connector.connect(host="localhost", user="service", password="storch",database='storch')
mycursor = mydb.cursor()

def updateConfig():
    global nextConfUpdate, pictureQuality, thumbFrequency, timelapseFrequency, configFrequency    
    nextConfUpdate = time.time()

    mycursor.execute("SELECT confvalue FROM config WHERE confkey = 'picture-quality'")
    pictureQuality = int(mycursor.fetchone()[0])

    mycursor.execute("SELECT confvalue FROM config WHERE confkey = 'thumb-frequency'")
    thumbFrequency = int(mycursor.fetchone()[0])

    mycursor.execute("SELECT confvalue FROM config WHERE confkey = 'timelapse-frequency'")
    timelapseFrequency = int(mycursor.fetchone()[0])

    mycursor.execute("SELECT confvalue FROM config WHERE confkey = 'picture-config-frequency'")
    configFrequency = int(mycursor.fetchone()[0])

    nextConfUpdate = nextConfUpdate + configFrequency



def takeImage():
    global nextPictureTime, pictureCounter, pictureQuality, thumbFrequency, timelapseFrequency   
    nextPictureTime = time.time()
    pictureCounter = pictureCounter + 1
    
    picStream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1440)
        camera.framerate = 10        
        camera.start_preview()
        time.sleep(10)    
        camera.capture(picStream, format='jpeg')
    
    picStream.seek(0)
    originalImage = Image.open(picStream)
    fullStream = io.BytesIO()
    originalImage.save(fullStream, format='jpeg',optimize=True,quality=pictureQuality)
    full_base64 = base64.encodebytes(fullStream.getvalue())
    fullStream.close()
    
    sql = "INSERT INTO pictures (full) VALUES (%s)"    
    sqlvalues = (full_base64,)    
    mycursor.execute(sql, sqlvalues)
    mydb.commit()

    if(pictureCounter >= thumbFrequency):
        pictureCounter = 0
        originalImage.thumbnail((192,144))
        thumbStream = io.BytesIO()
        originalImage.save(thumbStream, format='jpeg',optimize=True,quality=pictureQuality)    
        thumb_base64 = base64.encodebytes(thumbStream.getvalue())
        thumbStream.close()
        pictureId = mycursor.lastrowid
        sql = "INSERT INTO thumbs (thumb, pictureid) VALUES (%s,%s)"    
        sqlvalues = (thumb_base64, pictureId)        
        mycursor.execute(sql, sqlvalues)
        mydb.commit()
    
    picStream.close()    

    nextPictureTime = nextPictureTime + timelapseFrequency
    
if __name__ == "__main__":
    while(True):
        timeNow = time.time()
        if(timeNow >= nextConfUpdate):
            updateConfig()
        if (timeNow >= nextPictureTime):
            takeImage()
        time.sleep(1)
