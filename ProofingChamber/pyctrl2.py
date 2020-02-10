#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

sensor = '/sys/bus/w1/devices/28-011453efb2aa/w1_slave'
targetTemp = float(26.0)
integralFactor = float(0.8)
heatingTime = float(18.27)
cycleTime = float(50)

def readTempSensor(sensorName) :    
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTempLines(sensorName) :
    lines = readTempSensor(sensorName)    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')    
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        tempCelsius = float(tempData) / 1000.0        
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        return tempCelsius

try:
    while True :
        currentTemp = float(readTempLines(sensor))
        error = targetTemp - currentTemp        
        heatingTime = heatingTime + (integralFactor * error)
        if heatingTime < 0 :
            heatingTime = 0
        if heatingTime > cycleTime :
            heatingTime = cycleTime
        coolingTime = cycleTime - heatingTime
        with open("/home/pi/controller.log", "a") as logFile: 
            logFile.write(str(time.time_ns()) + " temperature=" + str(currentTemp) + " heating=" + str(heatingTime) + "\n")
        if heatingTime > 0 :
            GPIO.output(14, True)
            time.sleep(heatingTime)
        if coolingTime > 0 :
            GPIO.output(14, False)
            time.sleep(coolingTime)
except KeyboardInterrupt:    
    print('Temperaturmessung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    GPIO.cleanup()
    sys.exit(0)
