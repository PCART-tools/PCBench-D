    def __init__(self, *, status=200, reason=None, headers=None):
        self._body = None
        self._keep_alive = None
        self._chunked = False
        self._chunk_size = None
        self._compression = False
        self._compression_force = False
        self._headers = CIMultiDict()
        self._cookies = http.cookies.SimpleCookie()
        self.set_status(status, reason)

        self._req = None
        self._resp_impl = None
        self._eof_sent = False

        if headers is not None:
            self._headers.extend(headers)
        if hdrs.CONTENT_TYPE not in self._headers:
            self._headers[hdrs.CONTENT_TYPE] = 'application/octet-stream'
