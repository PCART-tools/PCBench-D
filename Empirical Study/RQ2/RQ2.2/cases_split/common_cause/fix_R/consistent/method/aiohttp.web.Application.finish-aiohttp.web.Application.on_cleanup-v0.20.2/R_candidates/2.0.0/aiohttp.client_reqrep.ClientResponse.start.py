    @asyncio.coroutine
    def start(self, connection, read_until_eof=False):
        """Start response processing."""
        self._closed = False
        self._protocol = connection.protocol
        self._connection = connection

        connection.protocol.set_response_params(
            timer=self._timer,
            skip_payload=self.method.lower() == 'head',
            skip_status_codes=(204, 304),
            read_until_eof=read_until_eof)

        with self._timer:
            while True:
                # read response
                (message, payload) = yield from self._protocol.read()
                if (message.code < 100 or
                        message.code > 199 or message.code == 101):
                    break

                if self._continue is not None and not self._continue.done():
                    self._continue.set_result(True)
                    self._continue = None

        # payload eof handler
        payload.on_eof(self._response_eof)

        # response status
        self.version = message.version
        self.status = message.code
        self.reason = message.reason

        # headers
        self.headers = CIMultiDictProxy(message.headers)
        self.raw_headers = tuple(message.raw_headers)

        # payload
        self.content = payload

        # cookies
        for hdr in self.headers.getall(hdrs.SET_COOKIE, ()):
            try:
                self.cookies.load(hdr)
            except CookieError as exc:
                client_logger.warning(
                    'Can not load response cookies: %s', exc)
        return self
