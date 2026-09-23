    def send_bytes(self, data):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        if self._closed:
            raise RuntimeError('websocket connection is closing')
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be byte-ish (%r)' %
                            type(data))
        self._writer.send(data, binary=True)
