    def __init__(self, *args):
        self._data = bytearray(*args)
        self._helper = _ParserBufferHelper(None, self._data)
        self._writer = self._feed_data(self._helper)
        next(self._writer)
