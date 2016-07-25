import os, sys
from twisted.web import static, server
# from multi_remote.gpio import GPIOHandler
# from multi_remote.service import Service

from twisted.python import log
from twisted.internet import reactor
from iot_twisted.service import Service

log.startLogging(sys.stdout)

Service(80, 22).startService()

reactor.run()
