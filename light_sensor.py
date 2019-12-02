try:
    import RPi.GPIO as GPIO
    import time

    GPIO.setmode(GPIO.BOARD)

    # define the pin that goes to the circuit
    pin_to_circuit = 11

    def door_open(pin_to_circuit):
        count = 0

        # Output on the pin for
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(1)

        # Change the pin back to input
        GPIO.setup(pin_to_circuit, GPIO.IN)

        # Count until the pin goes high
        while GPIO.input(pin_to_circuit) == GPIO.LOW:
            count += 1
            if count > 1700:
                break

        if count < 1500:
            return True
        else:
            return False

except ModuleNotFoundError:
    import random as rand
    import time
    print("Module Not Found")

    def door_open(some_number):
        time.sleep(1)
        count = rand.randint(0, 3000)
        if count < 1500:
            return True
        else:
            return False

if __name__ == '__main__':
    print(door_open(11))
