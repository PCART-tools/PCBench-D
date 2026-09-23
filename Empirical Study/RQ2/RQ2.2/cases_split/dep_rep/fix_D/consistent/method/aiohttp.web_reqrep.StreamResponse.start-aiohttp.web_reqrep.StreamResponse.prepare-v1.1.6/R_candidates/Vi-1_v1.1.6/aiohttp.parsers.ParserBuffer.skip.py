    def skip(self, size):
        """skip() skips specified amount of bytes."""

        while len(self._data) < size:
            if self._helper.exception:
                raise self._helper.exception

            self._writer.send((yield))

        del self._data[:size]
