    def read(self, size):
        """read() reads specified amount of bytes."""

        while True:
            if self._helper.exception:
                raise self._helper.exception

            if len(self._data) >= size:
                data = self._data[:size]
                del self._data[:size]
                return data

            self._writer.send((yield))
