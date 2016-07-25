import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class GPIOHandler(object):
    def __init__(self, pin):
        self.status = None
        self.pin = pin
        self.off()

    def on(self):
        self.__change(True)

    def off(self):
        self.__change(False)

    def __change(self, value):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, not value)
        self.status = value
