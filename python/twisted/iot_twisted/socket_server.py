import json
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.internet.defer import log


class ServerFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ServerFactory, self).__init__(*args, **kwargs)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            log.debug("registered client {peer}", peer=client.peer)
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            log.debug("unregistered client {client}", client=client)
            self.clients.remove(client)

    def broadcast(self, msg):
        log.debug("broadcasting prepared message '{msg}' ..", msg=msg)
        message = self.prepareMessage(msg)
        for c in self.clients:
            c.sendPreparedMessage(message)
            log.debug("prepared message sent to {peer}", peer=c.peer)


class ServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        log.debug("Client connecting: {peer}", peer=request.peer)
        self.factory.register(self)

    def onOpen(self):
        log.debug("WebSocket connection open.")
        # self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            log.debug("Binary message received: {bytes} bytes", bytes=len(payload))
            response = {'error': 'Protocol Error: unhandled message format'}
        else:
            message_string = payload.decode('utf8')
            log.debug("Text message received: {message}", message=message_string)
            message = json.loads(message_string)
            if 'action' in message:
                if 'status' == message['action']:
                    response = {'status': self.factory.led.status}
                elif 'set' == message['action']:
                    status = message.get('value')
                    try:
                        if status:
                            self.factory.led.on()
                        else:
                            self.factory.led.off()
                        response = {'status': status}
                        self.factory.broadcast(json.dumps(response, ensure_ascii=False).encode('utf8'))
                    except Exception as e:
                        log.error("Unable to update output: {error}", error=e)
                        pass

                    return
                else:
                    response = {'error': 'Protocol Error: unhandled action'}
            else:
                response = {'error': 'Protocol Error: unhandled verb'}

            response = json.dumps(response, ensure_ascii=False)

        self.sendMessage(response.encode('utf8'), isBinary=False)

    def onClose(self, wasClean, code, reason):
        self.factory.unregister(self)
        log.debug("WebSocket connection closed: {reason}", reason=reason)
