import io
import time
import picamera
import base64
import mysql.connector
from PIL import Image
from timeloop import Timeloop
from datetime import timedelta

# Change to loop with separate triggers for timelapse and web images


tl = Timeloop()

@tl.job(interval=timedelta(minutes=15))
def takeImage():
    mydb = mysql.connector.connect(host="localhost", user="service", password="storch",database='storch')
    mycursor = mydb.cursor()

    mycursor.execute("SELECT confvalue FROM config WHERE confkey = 'picture-quality'")
    pictureQuality = int(mycursor.fetchone()[0])

    picStream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (3280, 2464)
        camera.framerate = 5
        camera.start_preview()
        time.sleep(2)    
        camera.capture(picStream, format='jpeg')
    picStream.seek(0)
    originalImage = Image.open(picStream)

    fullImage = originalImage.resize((2000,1500))
    fullStream = io.BytesIO()
    fullImage.save(fullStream, format='jpeg',optimize=True,quality=pictureQuality)

    originalImage.thumbnail((240,180))

    thumbStream = io.BytesIO()
    originalImage.save(thumbStream, format='jpeg',optimize=True,quality=pictureQuality)
    picStream.close()

    thumb_base64 = base64.encodebytes(thumbStream.getvalue())
    full_base64 = base64.encodebytes(fullStream.getvalue())

    thumbStream.close()
    fullStream.close()

    sql = "INSERT INTO pictures (thumb, full) VALUES (%s, %s)"
    val = (thumb_base64, full_base64)
    mycursor.execute(sql, val)

    mydb.commit()
    
if __name__ == "__main__":
    tl.start(block=True)
    