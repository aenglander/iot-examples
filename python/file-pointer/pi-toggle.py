import os


def write(location, value):
    __file = open(location, "w")
    __file.write(value)
    __file.close()


def read(location):
    __file = open(location)
    __value = __file.read(1)
    return __value


if not os.path.exists("/sys/class/gpio/gpio18"):
    write("/sys/class/gpio/export", "18")
    write("/sys/class/gpio/gpio18/direction", "out")

current = read("/sys/class/gpio/gpio18/value")
if current == "1":
    write("/sys/class/gpio/gpio18/value", "0")
    print "off"
else:
    write("/sys/class/gpio/gpio18/value", "1")
    print "on"
