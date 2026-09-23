class ChunksParser:
    """Chunks parser.

    chunks parser splits a bytes stream into a specified
    size chunks of data."""

    def __init__(self, size=8196):
        self._size = size

    def __call__(self, out, buf):
        while True:
            out.feed_data((yield from buf.read(self._size)))
