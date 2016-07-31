from curio import run, spawn, run_in_thread, sleep
from curio.socket import *
from curio.file import *
import os
import mraa

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
            try:
                await run_in_thread(set_data, pin, value)
                result = "OK"
            except Exception as e:
                print("Error: {}".format(e))
                result = "ERROR"
            result += "\r\n"
            await client.sendall(result.encode())
    print('Connection closed')

def set_data(pin, value):
    gpio = mraa.Gpio(int(pin))
    gpio.dir(mraa.DIR_OUT)
    gpio.write(int(value))
    return gpio.read()

if __name__ == '__main__':
    try:
        run(echo_server(('0.0.0.0', 25000)))
    except KeyboardInterrupt:
        print("Exit requested via keyboard interrupt")
