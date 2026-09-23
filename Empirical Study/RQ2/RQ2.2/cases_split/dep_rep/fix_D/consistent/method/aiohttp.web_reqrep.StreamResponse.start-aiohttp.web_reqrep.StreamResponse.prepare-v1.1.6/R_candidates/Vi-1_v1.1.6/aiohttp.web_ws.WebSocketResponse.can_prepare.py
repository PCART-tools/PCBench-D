    def can_prepare(self, request):
        if self._writer is not None:
            raise RuntimeError('Already started')
        try:
            _, _, _, _, protocol = do_handshake(
                request.method, request.headers, request.transport,
                self._protocols)
        except HttpProcessingError:
            return WebSocketReady(False, None)
        else:
            return WebSocketReady(True, protocol)
