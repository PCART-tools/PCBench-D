    def close(self, code=1000, message=b''):
        """Close the websocket, sending the specified code and message."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        try:
            return self._send_frame(
                PACK_CLOSE_CODE(code) + message, opcode=WSMsgType.CLOSE)
        finally:
            self._closing = True
