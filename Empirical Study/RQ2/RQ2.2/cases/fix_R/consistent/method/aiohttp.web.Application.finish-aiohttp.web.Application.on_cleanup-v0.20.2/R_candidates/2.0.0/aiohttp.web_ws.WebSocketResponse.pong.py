    def pong(self, message='b'):
        # unsolicited pong
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        self._writer.pong(message)
