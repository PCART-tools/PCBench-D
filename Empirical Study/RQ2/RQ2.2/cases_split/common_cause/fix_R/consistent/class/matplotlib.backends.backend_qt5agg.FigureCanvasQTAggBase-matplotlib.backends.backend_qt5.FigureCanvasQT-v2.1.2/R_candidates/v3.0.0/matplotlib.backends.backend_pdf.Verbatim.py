class Verbatim(object):
    """Store verbatim PDF command content for later inclusion in the
    stream."""
    def __init__(self, x):
        self._x = x

    def pdfRepr(self):
        return self._x
