    @asyncio.coroutine
    def handle_request(self, message, payload):
        self._manager._requests_count += 1
        if self.access_log:
            now = self._loop.time()

        request = self._request_factory(message, payload, self)
        self._request = request

        try:
            try:
                resp = yield from self._handler(request)
            except HTTPException as exc:
                resp = exc
            except Exception as exc:
                msg = "<h1>500 Internal Server Error</h1>"
                if self.debug:
                    try:
                        tb = traceback.format_exc()
                        tb = html_escape(tb)
                        msg += '<br><h2>Traceback:</h2>\n<pre>'
                        msg += tb
                        msg += '</pre>'
                    except:  # pragma: no cover
                        pass
                else:
                    msg += "Server got itself in trouble"
                msg = ("<html><head><title>500 Internal Server Error</title>"
                       "</head><body>" + msg + "</body></html>")
                resp = HTTPInternalServerError(text=msg,
                                               content_type='text/html')
                self.logger.exception(
                    "Error handling request",
                    exc_info=exc)

            yield from resp.prepare(request)
            yield from resp.write_eof()
        finally:
            resp._task = None

        # notify server about keep-alive
        # assign to parent class attr
        self._keepalive = resp._keep_alive

        # Restore default state.
        # Should be no-op if server code didn't touch these attributes.
        self.writer.set_tcp_cork(False)
        self.writer.set_tcp_nodelay(True)

        # log access
        if self.access_log:
            self.log_access(message, None, resp, self._loop.time() - now)

        # for repr
        self._request = None
