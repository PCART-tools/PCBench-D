    def ping(self, message='b'):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        self._writer.ping(message)
