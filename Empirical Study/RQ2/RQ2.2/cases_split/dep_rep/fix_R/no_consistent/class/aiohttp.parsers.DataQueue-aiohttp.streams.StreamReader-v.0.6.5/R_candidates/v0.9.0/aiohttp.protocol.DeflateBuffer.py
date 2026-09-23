class DeflateBuffer:
    """DeflateStream decompress stream and feed data into specified stream."""

    def __init__(self, out, encoding):
        self.out = out
        zlib_mode = (16 + zlib.MAX_WBITS
                     if encoding == 'gzip' else -zlib.MAX_WBITS)

        self.zlib = zlib.decompressobj(wbits=zlib_mode)

    def feed_data(self, chunk):
        try:
            chunk = self.zlib.decompress(chunk)
        except Exception:
            raise errors.IncompleteRead(b'') from None

        if chunk:
            self.out.feed_data(chunk)

    def feed_eof(self):
        self.out.feed_data(self.zlib.flush())
        if not self.zlib.eof:
            raise errors.IncompleteRead(b'')

        self.out.feed_eof()
