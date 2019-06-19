from time import sleep
import picamera

WAIT_TIME = 30

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    for filename in camera.capture_continuous('/home/pi/time-lapse/img{timestamp:%Y-%m-%d-%H-%M-%S-%f}.jpg'):
        sleep(WAIT_TIME)

