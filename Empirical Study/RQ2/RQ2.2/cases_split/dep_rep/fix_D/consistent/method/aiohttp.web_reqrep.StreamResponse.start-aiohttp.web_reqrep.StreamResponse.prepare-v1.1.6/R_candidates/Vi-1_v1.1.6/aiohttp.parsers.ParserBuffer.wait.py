    def wait(self, size):
        """wait() waits for specified amount of bytes
        then returns data without changing internal buffer."""

        while True:
            if self._helper.exception:
                raise self._helper.exception

            if len(self._data) >= size:
                return self._data[:size]

            self._writer.send((yield))
