    def __init__(self, connector, key, request, transport, protocol, loop):
        self._key = key
        self._connector = connector
        self._request = request
        self._transport = transport
        self._protocol = protocol
        self._loop = loop
        self.reader = protocol.reader
        self.writer = protocol.writer

        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))
