    def __init__(self, transport, version, close):
        self.transport = transport
        self._version = version
        self.closing = close
        self.keepalive = None
        self.chunked = False
        self.length = None
        self.headers = CIMultiDict()
        self.headers_sent = False
        self.output_length = 0
        self.headers_length = 0
        self._output_size = 0
        self._cache = {}
