"""
This program gets readings from sensors

Author: Keith
Project: Fridge Tracker
"""
try:
    import Adafruit_DHT

    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4


    def get_reading():
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        return int(humidity), int(temperature)

except ModuleNotFoundError:
    print("Module Not Found")
    import random as rand
    import time

    def get_reading():
        time.sleep(1)
        return rand.randint(10, 50), rand.randint(0, 12)


if __name__ == '__main__':
    print(get_reading())
