class LinesParser:
    """Lines parser.

    Lines parser splits a bytes stream into a chunks of data, each chunk ends
    with \\n symbol."""

    def __init__(self, limit=2**16):
        self._limit = limit

    def __call__(self, out, buf):
        try:
            while True:
                out.feed_data((yield from buf.readuntil(b'\n', self._limit)))
        except EofStream:
            pass
