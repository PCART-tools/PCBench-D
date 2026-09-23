    def skipuntil(self, stop):
        """skipuntil() reads until `stop` bytes sequence."""
        assert isinstance(stop, bytes) and stop, \
            'bytes is required: {!r}'.format(stop)

        stop_len = len(stop)

        while True:
            if self._helper.exception:
                raise self._helper.exception

            stop_line = self._data.find(stop)
            if stop_line >= 0:
                size = stop_line + stop_len
                del self._data[:size]
                return

            self._writer.send((yield))
