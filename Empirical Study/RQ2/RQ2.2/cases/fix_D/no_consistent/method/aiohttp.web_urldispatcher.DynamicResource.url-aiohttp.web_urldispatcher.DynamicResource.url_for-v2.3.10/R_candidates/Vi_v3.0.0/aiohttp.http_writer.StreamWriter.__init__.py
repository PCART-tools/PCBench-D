    def __init__(self, protocol, transport, loop):
        self._protocol = protocol
        self._transport = transport

        self.loop = loop
        self.length = None
        self.chunked = False
        self.buffer_size = 0
        self.output_size = 0

        self._eof = False
        self._compress = None
        self._drain_waiter = None
