    def can_prepare(self, request):
        if self._writer is not None:
            raise RuntimeError('Already started')
        try:
            _, protocol, _, _ = self._handshake(request)
        except HTTPException:
            return WebSocketReady(False, None)
        else:
            return WebSocketReady(True, protocol)
