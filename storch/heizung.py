#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

sensor = '/sys/bus/w1/devices/28-01145074baaa/w1_slave'
targetTemp = float(30.0)
integralFactor = float(0.5)
cycleTime = float(15)

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
        return tempCelsius

try:
    currentTemp = float(readTempLines(sensor))
    heatingTime = 0
    error = targetTemp - currentTemp
    heatingTime = heatingTime + (integralFactor * error)
    if heatingTime < 2 :
        heatingTime = 0
    if heatingTime > cycleTime :
        heatingTime = cycleTime
    coolingTime = cycleTime - heatingTime
    cycle = 0
    while True :
        cycle = cycle + 1
        currentTemp = float(readTempLines(sensor))
        if cycle >= 4 :
            error = targetTemp - currentTemp
            heatingTime = heatingTime + (integralFactor * error)
            if heatingTime < 0 :
                heatingTime = 0
            if heatingTime > cycleTime :
                heatingTime = cycleTime
            coolingTime = cycleTime - heatingTime
            cycle = 0
        if heatingTime > 0 :
            GPIO.output(14, True)
            time.sleep(heatingTime)
        if coolingTime > 0 :
            GPIO.output(14, False)
            time.sleep(coolingTime)
except KeyboardInterrupt:    
    print('Temperatursteuerung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    GPIO.cleanup()
    sys.exit(0)
