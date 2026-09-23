    def readuntil(self, stop, limit=None):
        assert isinstance(stop, bytes) and stop, \
            'bytes is required: {!r}'.format(stop)

        stop_len = len(stop)

        while True:
            if self._helper.exception:
                raise self._helper.exception

            pos = self._data.find(stop)
            if pos >= 0:
                end = pos + stop_len
                size = end
                if limit is not None and size > limit:
                    raise errors.LineLimitExceededParserError(
                        'Line is too long.', limit)

                data = self._data[:size]
                del self._data[:size]
                return data
            else:
                if limit is not None and len(self._data) > limit:
                    raise errors.LineLimitExceededParserError(
                        'Line is too long.', limit)

            self._writer.send((yield))
