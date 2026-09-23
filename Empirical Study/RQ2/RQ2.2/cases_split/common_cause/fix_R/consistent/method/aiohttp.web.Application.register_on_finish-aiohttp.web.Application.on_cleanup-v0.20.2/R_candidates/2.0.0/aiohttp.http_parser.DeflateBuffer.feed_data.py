    def feed_data(self, chunk, size):
        self.size += size
        try:
            chunk = self.zlib.decompress(chunk)
        except Exception:
            raise ContentEncodingError(
                'Can not decode content-encoding: %s' % self.encoding)

        if chunk:
            self.out.feed_data(chunk, len(chunk))
