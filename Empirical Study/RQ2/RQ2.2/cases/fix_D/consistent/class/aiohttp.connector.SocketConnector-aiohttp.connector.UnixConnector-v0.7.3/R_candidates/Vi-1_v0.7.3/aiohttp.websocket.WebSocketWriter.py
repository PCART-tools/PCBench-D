class WebSocketWriter:

    def __init__(self, writer):
        self.writer = writer

    def _send_frame(self, message, opcode):
        """Send a frame over the websocket with message as its payload."""
        header = bytes([0x80 | opcode])
        msg_length = len(message)

        if msg_length < 126:
            header += bytes([msg_length])
        elif msg_length < (1 << 16):
            header += bytes([126]) + struct.pack('!H', msg_length)
        else:
            header += bytes([127]) + struct.pack('!Q', msg_length)

        self.writer.write(header + message)

    def pong(self):
        """Send pong message."""
        self._send_frame(b'', OPCODE_PONG)

    def ping(self):
        """Send pong message."""
        self._send_frame(b'', OPCODE_PING)

    def send(self, message, binary=False):
        """Send a frame over the websocket with message as its payload."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        if binary:
            self._send_frame(message, OPCODE_BINARY)
        else:
            self._send_frame(message, OPCODE_TEXT)

    def close(self, code=1000, message=b''):
        """Close the websocket, sending the specified code and message."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        self._send_frame(
            struct.pack('!H%ds' % len(message), code, message),
            opcode=OPCODE_CLOSE)
