import os
from autobahn.twisted.resource import WebSocketResource
from twisted.application import service
from twisted.internet import reactor
from twisted.web import static, server
from iot_twisted.gpio import GPIOHandler
from iot_twisted.socket_server import ServerFactory, ServerProtocol


class Service(service.Service):
    def __init__(self, port, pin):
        self.port = port
        self.server = None
        self.pin = pin

    def startService(self):
        root = static.File(os.path.join(os.path.dirname(__file__), 'public'))

        factory = ServerFactory()
        factory.status = False
        factory.led = GPIOHandler(self.pin)
        factory.protocol = ServerProtocol
        # factory.setProtocolOptions(maxConnections=2)
        factory.startFactory()
        resource = WebSocketResource(factory)
        root.putChild('socket', resource)

        site = server.Site(root)

        self.server = reactor.listenTCP(self.port, site)

    def stopService(self):
        return self.server.stopListening()
