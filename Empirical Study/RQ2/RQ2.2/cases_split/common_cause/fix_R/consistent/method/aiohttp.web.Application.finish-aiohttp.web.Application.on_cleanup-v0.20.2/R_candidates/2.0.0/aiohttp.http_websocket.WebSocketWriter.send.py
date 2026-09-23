    def send(self, message, binary=False):
        """Send a frame over the websocket with message as its payload."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        if binary:
            return self._send_frame(message, WSMsgType.BINARY)
        else:
            return self._send_frame(message, WSMsgType.TEXT)
