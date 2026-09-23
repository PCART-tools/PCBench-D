    def __init__(self, out, encoding):
        self.out = out
        self.size = 0
        self.encoding = encoding

        zlib_mode = (16 + zlib.MAX_WBITS
                     if encoding == 'gzip' else -zlib.MAX_WBITS)

        self.zlib = zlib.decompressobj(wbits=zlib_mode)
