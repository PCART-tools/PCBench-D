    def feed_data(self, data, size):
        super().feed_data(data, size)

        if self._size > self._limit and not self._protocol._reading_paused:
            self._protocol.pause_reading()
