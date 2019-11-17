"""
This program gets readings from sensors

Author: Keith
Project: Fridge Tracker
"""
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4


def get_reading():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
