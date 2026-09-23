    def ping(self, message='b'):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        if self._closed:
            raise RuntimeError('websocket connection is closing')
        self._writer.ping(message)
