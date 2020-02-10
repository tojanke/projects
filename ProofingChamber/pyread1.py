#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(14, GPIO.OUT)

sensor1 = '/sys/bus/w1/devices/28-011453efb2aa/w1_slave'
sensor2 = '/sys/bus/w1/devices/28-0114543197aa/w1_slave'
enabled = false

def readTempSensor(sensorName) :
    """Aus dem Systembus lese ich die Temperatur der DS18B20 aus."""
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTempLines(sensorName) :
    lines = readTempSensor(sensorName)
    # Solange nicht die Daten gelesen werden konnten, bin ich hier in einer Endlosschleife
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    # Ich überprüfe ob die Temperatur gefunden wurde.
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        tempCelsius = float(tempData) / 1000.0
        tempKelvin = 273 + float(tempData) / 1000
        tempFahrenheit = float(tempData) / 1000 * 9.0 / 5.0 + 32.0
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        return [tempCelsius, tempKelvin, tempFahrenheit]

try:
    while True :
        # Mit einem Timestamp versehe ich meine Messung und lasse mir diese in der Console ausgeben.
        print("Temperatur um " + time.strftime('%H:%M:%S') +": " + str(readTempLines(sensor1)[0]) + " °C / " + str(readTempLines(sensor2)[0]) + " °C")
        GPIO.output(14, enabled)
        enabled = not enabled
        # Nach 10 Sekunden erfolgt die nächste Messung
        time.sleep(2)
except KeyboardInterrupt:    
    GPIO.cleanup()
    sys.exit(1)
except Exception as e:
    print(str(e))
    GPIO.cleanup()
    sys.exit(1)
finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    GPIO.cleanup()
    sys.exit(0)
