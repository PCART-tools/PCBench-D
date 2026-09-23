    def __init__(self, protocol, *, limit=DEFAULT_LIMIT, loop=None):
        super().__init__(loop=loop)

        self._protocol = protocol
        self._limit = limit * 2
