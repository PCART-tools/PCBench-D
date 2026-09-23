    def ping(self, message=b''):
        """Send ping message."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        return self._send_frame(message, WSMsgType.PING)
