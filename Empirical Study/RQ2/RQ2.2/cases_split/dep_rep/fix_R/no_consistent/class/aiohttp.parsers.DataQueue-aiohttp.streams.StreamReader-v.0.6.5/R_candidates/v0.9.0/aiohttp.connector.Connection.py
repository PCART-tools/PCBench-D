class Connection(object):

    def __init__(self, connector, key, request, transport, protocol, loop):
        self._key = key
        self._connector = connector
        self._request = request
        self._transport = transport
        self._protocol = protocol
        self._loop = loop
        self.reader = protocol.reader
        self.writer = protocol.writer
        self._wr = weakref.ref(self, lambda wr, tr=self._transport: tr.close())

    @property
    def loop(self):
        return self._loop

    def close(self):
        if self._transport is not None:
            self._transport.close()
            self._transport = None
            self._wr = None

    def release(self):
        if self._transport:
            self._connector._release(
                self._key, self._request, self._transport, self._protocol)
            self._transport = None
            self._wr = None
