from os import path
from sys import platform

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='iot-example-twisted',
    version='0.0.1',
    author='Adam Englander',
    author_email='adam@launchkey.com',
    url='https://launchkey.com',
    summary='IoT Example for Twisted',
    license='MIT',
    description='An example for IoT in Twisted',
    install_requires=['autobahn', 'twisted', 'pyOpenSSL', 'RPi.GPIO', 'service-identity'],
    data_files=[]
)
