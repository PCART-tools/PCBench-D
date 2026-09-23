    def _pre_start(self, request):
        self._loop = request.app.loop

        try:
            status, headers, _, writer, protocol = do_handshake(
                request.method, request.headers, request._protocol.writer,
                self._protocols)
        except HttpProcessingError as err:
            if err.code == 405:
                raise HTTPMethodNotAllowed(
                    request.method, [hdrs.METH_GET], body=b'')
            elif err.code == 400:
                raise HTTPBadRequest(text=err.message, headers=err.headers)
            else:  # pragma: no cover
                raise HTTPInternalServerError() from err

        self._reset_heartbeat()

        if self.status != status:
            self.set_status(status)
        for k, v in headers:
            self.headers[k] = v
        self.force_close()
        return protocol, writer
