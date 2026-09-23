    def feed_data(self, data):
        if self._exc:
            return True, data

        try:
            return self._feed_data(data)
        except Exception as exc:
            self._exc = exc
            self.queue.set_exception(exc)
            return True, b''
