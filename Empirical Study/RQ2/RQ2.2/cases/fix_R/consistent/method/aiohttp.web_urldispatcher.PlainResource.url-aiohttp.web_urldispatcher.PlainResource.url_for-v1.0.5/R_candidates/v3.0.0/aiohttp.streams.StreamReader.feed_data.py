    def feed_data(self, data, size=0):
        assert not self._eof, 'feed_data after feed_eof'

        if not data:
            return

        self._size += len(data)
        self._buffer.append(data)
        self.total_bytes += len(data)

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            set_result(waiter, False)

        if (self._size > self._high_water and
                not self._protocol._reading_paused):
            self._protocol.pause_reading()
