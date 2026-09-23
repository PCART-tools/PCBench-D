    def feed_data(self, data, size):
        has_waiter = self._waiter is not None and not self._waiter.cancelled()

        super().feed_data(data, size)

        if (not self._stream.paused and
                not has_waiter and self._size > self._limit):
            try:
                self._stream.transport.pause_reading()
            except (AttributeError, NotImplementedError):
                pass
            else:
                self._stream.paused = True
