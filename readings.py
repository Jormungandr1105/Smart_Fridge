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
        return float(humidity), float(temperature)

except ModuleNotFoundError:
    print("Module Not Found")
    import random as rand
    import time

    def get_reading():
        time.sleep(1)
        return rand.uniform(10, 50), rand.uniform(0, 12)


if __name__ == '__main__':
    for x in range(10):
        humidity, temperature = get_reading()
        print("Temperature: {:.0f}°C\tHumidity: {:.0f}%".format(temperature, humidity))
