    def __init__(self, *, status=200, reason=None, headers=None):
        self._body = None
        self._keep_alive = None
        self._chunked = False
        self._compression = False
        self._compression_force = False
        self._cookies = SimpleCookie()

        self._req = None
        self._payload_writer = None
        self._eof_sent = False
        self._body_length = 0

        if headers is not None:
            self._headers = CIMultiDict(headers)
        else:
            self._headers = CIMultiDict()

        self.set_status(status, reason)
