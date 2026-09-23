    def feed_data(self, data, size=0):
        has_waiter = self._waiter is not None and not self._waiter.cancelled()

        super().feed_data(data)

        if (not self._stream.paused and
                not has_waiter and self._buffer_size > self._b_limit):
            try:
                self._stream.transport.pause_reading()
            except (AttributeError, NotImplementedError):
                pass
            else:
                self._stream.paused = True
