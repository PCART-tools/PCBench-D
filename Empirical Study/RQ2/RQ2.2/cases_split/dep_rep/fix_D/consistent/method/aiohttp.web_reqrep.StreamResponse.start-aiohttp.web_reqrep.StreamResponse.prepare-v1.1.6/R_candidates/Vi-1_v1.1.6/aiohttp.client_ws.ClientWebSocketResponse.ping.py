    def ping(self, message='b'):
        if self._closed:
            raise RuntimeError('websocket connection is closed')
        self._writer.ping(message)
