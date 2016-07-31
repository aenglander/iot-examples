from curio import run, spawn, run_in_thread, sleep
from curio.socket import *
from curio.file import *
import os

async def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print('Server listening at', address)
    async with sock:
        while True:
            client, addr = await sock.accept()
            await spawn(iot_client(client, addr))


async def iot_client(client, addr):
    print('Connection from', addr)
    async with client:
        while True:
            data = await client.recv(5)
            if not data:
                break

            pin = data[:2].decode()
            value = data[2:3].decode()
            print("Preparing pin {} if necessary".format(pin))
            await prep_pin(pin)
            print("Writing value \"{}\" to pin {}".format(value, pin))
            await write_pin_data(pin, value)
            new_value = await read_pin_data(pin)
            result = "OK" if new_value == value else "ERROR"
            result += "\r\n"
            await client.sendall(result.encode())
    print('Connection closed')

async def prep_pin(pin):
    if not await run_in_thread(os.path.exists, u"/sys/class/gpio/gpio".format(pin)):
        async with aopen("/sys/class/gpio/export", "w") as export:
            await export.write(pin)
            print("Pin {} exported...waiting for direction file to appear".format(pin))
            direction_file = u"/sys/class/gpio/gpio{}/direction".format(pin)
            while not await run_in_thread(os.path.isfile, direction_file):
                await sleep(0)
            print("Direction file found. Setting direction out for pin".format(pin))
            async with aopen(direction_file, "w") as direction:
                await direction.write("out")
            print("Direction written for pin {}".format(pin))
            return None

async def write_pin_data(pin, value):
    print(u'Writing "{}" to pin {}'.format(value, pin))
    async with aopen(u"/sys/class/gpio/gpio{}/value".format(pin), "w") as pin_file:
        return await pin_file.write(value)


async def read_pin_data(pin):
    async with aopen(u"/sys/class/gpio/gpio{}/value".format(pin), "r") as pin_file:
        value = await pin_file.read()
        print('Pin {} now has value of "{}"'.format(pin, value))
        return value


if __name__ == '__main__':
    try:
        run(echo_server(('0.0.0.0', 25000)))
    except KeyboardInterrupt:
        print("Exit requested via keyboard interrupt")
