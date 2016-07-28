import os

import time


class GPIOHandler(object):
    def __init__(self, pin):
        self.status = None
        self.pin = pin
        self.__gpio_dir = "/sys/class/gpio/gpio{}".format(pin)
        self.__value_file = "{}/value".format(self.__gpio_dir)
        self.__setup()
        self.off()

    def on(self):
        self.__change(True)

    def off(self):
        self.__change(False)

    def __change(self, value):
        self.__write_data(self.__value_file, "1" if value else "0")
        self.status = value

    def __setup(self):
        counter = 0

        if not os.path.isdir(self.__gpio_dir):
            with open("/sys/class/gpio/export", "w") as export:
                export.write(str(self.pin))

        direction = "{}/direction".format(self.__gpio_dir)
        while not os.path.isfile(direction) and counter < 1000:
            time.sleep(0.01)
            counter += 1
        GPIOHandler.__write_data(direction, "out")

    @staticmethod
    def __write_data(location, value):
        with open(location, "w") as fd:
            fd.write(value)
