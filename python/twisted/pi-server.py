import os, sys
from twisted.web import static, server

from twisted.python import log
from twisted.internet import reactor
from iot_twisted.service import Service

log.startLogging(sys.stdout)

Service(8080, 18).startService()

reactor.run()
