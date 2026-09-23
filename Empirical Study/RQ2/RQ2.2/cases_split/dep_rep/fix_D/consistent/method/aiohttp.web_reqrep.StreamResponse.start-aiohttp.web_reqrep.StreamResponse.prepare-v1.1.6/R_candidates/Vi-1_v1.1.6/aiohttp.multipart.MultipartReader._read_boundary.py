    @asyncio.coroutine
    def _read_boundary(self):
        chunk = (yield from self._readline()).rstrip()
        if chunk == self._boundary:
            pass
        elif chunk == self._boundary + b'--':
            self._at_eof = True
        else:
            raise ValueError('Invalid boundary %r, expected %r'
                             % (chunk, self._boundary))
