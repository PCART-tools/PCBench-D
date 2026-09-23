    def waituntil(self, stop, limit=None):
        """waituntil() reads until `stop` bytes sequence."""
        assert isinstance(stop, bytes) and stop, \
            'bytes is required: {!r}'.format(stop)

        stop_len = len(stop)

        while True:
            if self._helper.exception:
                raise self._helper.exception

            pos = self._data.find(stop)
            if pos >= 0:
                size = pos + stop_len
                if limit is not None and size > limit:
                    raise errors.LineLimitExceededParserError(
                        'Line is too long. %s' % bytes(self._data), limit)

                return self._data[:size]
            else:
                if limit is not None and len(self._data) > limit:
                    raise errors.LineLimitExceededParserError(
                        'Line is too long. %s' % bytes(self._data), limit)

            self._writer.send((yield))
