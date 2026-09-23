    def handle_request(self, message, payload):
        """Handle a single HTTP request.

        Subclass should override this method. By default it always
        returns 404 response.

        :param message: Request headers
        :type message: aiohttp.protocol.HttpRequestParser
        :param payload: Request payload
        :type payload: aiohttp.streams.FlowControlStreamReader
        """
        now = self._loop.time()
        response = aiohttp.Response(
            self.writer, 404, http_version=message.version, close=True)

        body = b'Page Not Found!'

        response.add_header(hdrs.CONTENT_TYPE, 'text/plain')
        response.add_header(hdrs.CONTENT_LENGTH, str(len(body)))
        response.send_headers()
        response.write(body)
        drain = response.write_eof()

        self.keep_alive(False)
        self.log_access(message, None, response, self._loop.time() - now)

        return drain
