class LinesParser:
    """Lines parser.

    lines parser splits a bytes stream into a chunks of data, each chunk ends
    with \n symbol."""

    def __init__(self, limit=2**16, exc=ValueError):
        self._limit = limit
        self._exc = exc

    def __call__(self, out, buf):
        while True:
            out.feed_data(
                (yield from buf.readuntil(b'\n', self._limit, self._exc)))
