from http.client import RemoteDisconnected

from gpiozero import Button, OutputDevice
import RPi.GPIO as GPIO
from dht11 import DHT11
import glob
import time
from threading import Thread

import influxdb_client, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "tojanke"
url = "https://influx.tojanke.de"

influx_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
influx_api = influx_client.write_api(write_options=SYNCHRONOUS)

w1_base_dir = '/sys/bus/w1/devices/'
temp_sensor_folder = glob.glob(w1_base_dir + '28*')[0]
temp_sensor_file = temp_sensor_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)

button = Button(17)
humidity_sensor = DHT11(pin=2)
water_switch = Button(4)
fan = OutputDevice(14)
compressor = OutputDevice(15)
pump = OutputDevice(18)

target_humidity = 55

def readTempSensor():
    f = open(temp_sensor_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

cooler_temp = 20

def getCoolerTemperature():
    global cooler_temp
    lines = readTempSensor()
    while len(lines) < 2 or lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor()
    temperaturStr = lines[1].find('t=')
    if temperaturStr != -1:
        tempData = lines[1][temperaturStr + 2:]
        tempCelsius = float(tempData) / 1000.0
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        if tempCelsius != 85.0:
            cooler_temp = tempCelsius

humidity = float(60.0)
air_temp = float(20.0)

def getHumidityAndAirTemperature():
    global humidity, air_temp
    result = humidity_sensor.read()
    tries = 0
    while not result.is_valid() and tries < 10:
        time.sleep(2)
        result = humidity_sensor.read()
        tries += 1
    if result.is_valid():
        humidity, air_temp = result.humidity, result.temperature

run_pump_until = 0
compressor_cooldown_until = 0

tank_capacity = 10000.0
pump_ml_per_second = 12.5
pump_cycle = 500.0

pumped = 0.0
next_influx_write = 0

next_measurement = 0

def measurementFunction():
    global next_measurement, next_influx_write
    while True:
        now = time.time()
        if next_measurement < now:
            getCoolerTemperature()
            getHumidityAndAirTemperature()
            next_measurement = now + 30

measurementThread = Thread(target=measurementFunction)
measurementThread.start()

def reportFunction():
    global next_influx_write
    while True:
        now = time.time()
        if next_influx_write < now:
            point = (
                Point("dehumidifier")
                .field("cooler_temp", float(cooler_temp))
                .field("humidity", float(humidity))
                .field("air_temp", float(air_temp))
                .field("pumped", int(pumped))
                .field("compressor_on", compressor.is_active)
                .field("fan_on", fan.is_active)
                .field("pump_on", pump.is_active)
                .field("water_sw", water_switch.is_active)
            )
            try:
                influx_api.write(bucket="tojanke", org="tojanke", record=point)
            except RemoteDisconnected:
                print("Network problems")
            next_influx_write = now + 20

reportThread = Thread(target=reportFunction)
reportThread.start()

while True:
    now = time.time()

    if not 1 < cooler_temp < 60 and compressor.is_active:
        print("Compressor off, temperature is " + str(cooler_temp))
        compressor.off()
        compressor_cooldown_until = now + 600
    elif humidity < target_humidity and compressor.is_active:
        print("Humidity low, stopping compressor")
        compressor.off()
        compressor_cooldown_until = now + 900
    elif not water_switch.is_active and compressor.is_active:
        print("Water full, stopping compressor")
        compressor.off()
        compressor_cooldown_until = now + 60
    elif water_switch.is_active and compressor_cooldown_until < now and not compressor.is_active:
        print("Starting Compressor")
        compressor.on()

    if humidity > target_humidity and not fan.is_active:
        print("Starting Fan")
        fan.on()
    elif (humidity < target_humidity or not water_switch.is_active) and fan.is_active:
        print("Stopping Fan")
        fan.off()

    if run_pump_until < now and pump.is_active:
        print("Stopping Pump")
        pump.off()
    elif not water_switch.is_active and pumped < tank_capacity and not pump.is_active:
        print("Starting Pump")
        pump.on()
        cycle = min(pump_cycle, tank_capacity - pumped)
        run_pump_until = now + cycle / pump_ml_per_second
        pumped += cycle

    if button.is_active:
        print("Resetting pumps")
        pumped = 0
        time.sleep(2)