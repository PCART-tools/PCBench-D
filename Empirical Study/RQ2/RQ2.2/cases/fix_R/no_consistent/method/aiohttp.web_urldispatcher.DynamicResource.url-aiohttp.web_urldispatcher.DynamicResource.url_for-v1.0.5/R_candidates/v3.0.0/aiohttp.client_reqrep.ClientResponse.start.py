    async def start(self, connection, read_until_eof=False):
        """Start response processing."""
        self._closed = False
        self._protocol = connection.protocol
        self._connection = connection

        connection.protocol.set_response_params(
            timer=self._timer,
            skip_payload=self.method.lower() == 'head',
            read_until_eof=read_until_eof,
            auto_decompress=self._auto_decompress)

        with self._timer:
            while True:
                # read response
                try:
                    (message, payload) = await self._protocol.read()
                except http.HttpProcessingError as exc:
                    raise ClientResponseError(
                        self.request_info, self.history,
                        code=exc.code,
                        message=exc.message, headers=exc.headers) from exc

                if (message.code < 100 or
                        message.code > 199 or message.code == 101):
                    break

                if self._continue is not None:
                    set_result(self._continue, True)
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
