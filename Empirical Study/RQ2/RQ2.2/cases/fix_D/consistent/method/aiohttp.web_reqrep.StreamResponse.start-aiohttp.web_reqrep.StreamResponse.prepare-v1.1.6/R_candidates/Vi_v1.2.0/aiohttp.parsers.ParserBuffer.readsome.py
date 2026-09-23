    def readsome(self, size=None):
        """reads size of less amount of bytes."""

        while True:
            if self._helper.exception:
                raise self._helper.exception

            length = len(self._data)
            if length > 0:
                if size is None or length < size:
                    size = length

                data = self._data[:size]
                del self._data[:size]
                return data

            self._writer.send((yield))
