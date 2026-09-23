    def handle_error(self, status=500, message=None,
                     payload=None, exc=None, headers=None, reason=None):
        """Handle errors.

        Returns HTTP response with specific status code. Logs additional
        information. It always closes current connection."""
        now = self._loop.time()
        try:
            if self.transport is None:
                # client has been disconnected during writing.
                return ()

            if status == 500:
                self.log_exception("Error handling request")

            try:
                if reason is None or reason == '':
                    reason, msg = RESPONSES[status]
                else:
                    msg = reason
            except KeyError:
                status = 500
                reason, msg = '???', ''

            if self.debug and exc is not None:
                try:
                    tb = traceback.format_exc()
                    tb = html_escape(tb)
                    msg += '<br><h2>Traceback:</h2>\n<pre>{}</pre>'.format(tb)
                except:
                    pass

            html = DEFAULT_ERROR_MESSAGE.format(
                status=status, reason=reason, message=msg).encode('utf-8')

            response = aiohttp.Response(self.writer, status, close=True)
            response.add_header(hdrs.CONTENT_TYPE, 'text/html; charset=utf-8')
            response.add_header(hdrs.CONTENT_LENGTH, str(len(html)))
            if headers is not None:
                for name, value in headers:
                    response.add_header(name, value)
            response.send_headers()

            response.write(html)
            # disable CORK, enable NODELAY if needed
            self.writer.set_tcp_nodelay(True)
            drain = response.write_eof()

            self.log_access(message, None, response, self._loop.time() - now)
            return drain
        finally:
            self.keep_alive(False)
