    def send_bytes(self, data):
        if self._closed:
            raise RuntimeError('websocket connection is closed')
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be byte-ish (%r)' %
                            type(data))
        self._writer.send(data, binary=True)
