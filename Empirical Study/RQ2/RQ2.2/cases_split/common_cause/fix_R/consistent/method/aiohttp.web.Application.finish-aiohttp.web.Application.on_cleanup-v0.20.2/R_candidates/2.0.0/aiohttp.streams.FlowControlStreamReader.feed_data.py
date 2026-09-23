    def feed_data(self, data, size=0):
        super().feed_data(data)

        if self._size > self._b_limit and not self._protocol._reading_paused:
            self._protocol.pause_reading()
