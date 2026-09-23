    def pong(self, message=b''):
        """Send pong message."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        self._send_frame(message, WSMsgType.PONG)
