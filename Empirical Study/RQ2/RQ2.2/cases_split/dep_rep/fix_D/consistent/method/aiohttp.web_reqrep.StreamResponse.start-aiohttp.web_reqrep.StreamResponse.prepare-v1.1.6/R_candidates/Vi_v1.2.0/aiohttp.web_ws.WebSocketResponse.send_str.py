    def send_str(self, data):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        if self._closed:
            raise RuntimeError('websocket connection is closing')
        if not isinstance(data, str):
            raise TypeError('data argument must be str (%r)' % type(data))
        self._writer.send(data, binary=False)
