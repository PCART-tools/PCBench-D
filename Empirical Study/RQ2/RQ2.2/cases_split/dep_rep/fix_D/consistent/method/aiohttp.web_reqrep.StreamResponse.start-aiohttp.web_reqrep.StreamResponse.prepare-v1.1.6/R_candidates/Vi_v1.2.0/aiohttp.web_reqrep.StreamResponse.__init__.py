    def __init__(self, *, status=200, reason=None, headers=None):
        self._body = None
        self._keep_alive = None
        self._chunked = False
        self._chunk_size = None
        self._compression = False
        self._compression_force = False
        self._headers = CIMultiDict()
        self._cookies = SimpleCookie()

        self._req = None
        self._resp_impl = None
        self._eof_sent = False

        self._task = None

        if headers is not None:
            # TODO: optimize CIMultiDict extending
            self._headers.extend(headers)
        self._headers.setdefault(hdrs.CONTENT_TYPE, 'application/octet-stream')

        self.set_status(status, reason)
