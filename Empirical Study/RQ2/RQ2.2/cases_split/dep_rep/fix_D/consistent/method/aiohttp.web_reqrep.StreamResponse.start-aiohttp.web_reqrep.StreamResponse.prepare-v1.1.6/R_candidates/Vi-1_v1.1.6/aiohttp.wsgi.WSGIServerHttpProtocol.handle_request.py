    @asyncio.coroutine
    def handle_request(self, message, payload):
        """Handle a single HTTP request"""
        now = self._loop.time()

        if self.readpayload:
            wsgiinput = io.BytesIO()
            wsgiinput.write((yield from payload.read()))
            wsgiinput.seek(0)
            payload = wsgiinput

        environ = self.create_wsgi_environ(message, payload)
        response = self.create_wsgi_response(message)

        riter = self.wsgi(environ, response.start_response)
        if isinstance(riter, asyncio.Future) or inspect.isgenerator(riter):
            riter = yield from riter

        resp = response.response
        try:
            for item in riter:
                if isinstance(item, asyncio.Future):
                    item = yield from item
                yield from resp.write(item)

            yield from resp.write_eof()
        finally:
            if hasattr(riter, 'close'):
                riter.close()

        if resp.keep_alive():
            self.keep_alive(True)

        self.log_access(
            message, environ, response.response, self._loop.time() - now)
