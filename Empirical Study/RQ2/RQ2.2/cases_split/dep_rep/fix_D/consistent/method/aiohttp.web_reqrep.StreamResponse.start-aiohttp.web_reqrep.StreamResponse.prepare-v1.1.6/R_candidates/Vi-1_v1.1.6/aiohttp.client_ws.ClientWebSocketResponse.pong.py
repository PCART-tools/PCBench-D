    def pong(self, message='b'):
        if self._closed:
            raise RuntimeError('websocket connection is closed')
        self._writer.pong(message)
