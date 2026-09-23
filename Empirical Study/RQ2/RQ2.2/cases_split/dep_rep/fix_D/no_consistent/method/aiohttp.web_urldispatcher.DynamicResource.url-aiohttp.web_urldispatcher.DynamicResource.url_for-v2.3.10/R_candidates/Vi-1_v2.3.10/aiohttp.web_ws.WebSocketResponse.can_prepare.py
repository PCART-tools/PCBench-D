    def can_prepare(self, request):
        if self._writer is not None:
            raise RuntimeError('Already started')
        try:
            _, _, _, _, protocol, _ = do_handshake(
                request.method, request.headers, request._protocol.writer,
                self._protocols)
        except HttpProcessingError:
            return WebSocketReady(False, None)
        else:
            return WebSocketReady(True, protocol)
