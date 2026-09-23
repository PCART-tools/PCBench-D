    @asyncio.coroutine
    def start(self, connection, read_until_eof=False):
        """Start response processing."""
        self._setup_connection(connection)

        while True:
            httpstream = self._reader.set_parser(self._response_parser)

            # read response
            with Timeout(self._timeout, loop=self._loop):
                message = yield from httpstream.read()
            if message.code != 100:
                break

            if self._continue is not None and not self._continue.done():
                self._continue.set_result(True)
                self._continue = None

        # response status
        self.version = message.version
        self.status = message.code
        self.reason = message.reason
        self._should_close = message.should_close

        # headers
        self.headers = CIMultiDictProxy(message.headers)
        self.raw_headers = tuple(message.raw_headers)

        # payload
        rwb = self._need_parse_response_body()
        self._reader.set_parser(
            aiohttp.HttpPayloadParser(message,
                                      readall=read_until_eof,
                                      response_with_body=rwb),
            self.content)

        # cookies
        for hdr in self.headers.getall(hdrs.SET_COOKIE, ()):
            try:
                self.cookies.load(hdr)
            except http.cookies.CookieError as exc:
                client_logger.warning(
                    'Can not load response cookies: %s', exc)
        return self
