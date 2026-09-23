    def __init__(self, out, encoding):
        self.out = out
        self.size = 0
        self.encoding = encoding
        self._started_decoding = False

        if encoding == 'br':
            if not HAS_BROTLI:  # pragma: no cover
                raise ContentEncodingError(
                    'Can not decode content-encoding: brotli (br). '
                    'Please install `brotlipy`')
            self.decompressor = brotli.Decompressor()
        else:
            zlib_mode = (16 + zlib.MAX_WBITS
                         if encoding == 'gzip' else -zlib.MAX_WBITS)
            self.decompressor = zlib.decompressobj(wbits=zlib_mode)
