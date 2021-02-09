from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1920, 1080)
i = 1

while True:    
    camera.start_preview()
    sleep(2)
    camera.capture(str(i).zfill(5) + '.jpg')
    camera.stop_preview()
    print(str(i).zfill(5) + '.jpg')
    i = i+1
    sleep(28)