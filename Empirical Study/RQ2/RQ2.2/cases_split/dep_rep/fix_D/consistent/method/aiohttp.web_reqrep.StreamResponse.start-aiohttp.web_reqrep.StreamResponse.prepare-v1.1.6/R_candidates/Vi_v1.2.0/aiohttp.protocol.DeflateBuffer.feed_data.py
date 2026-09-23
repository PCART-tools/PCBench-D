    def feed_data(self, chunk, size):
        try:
            chunk = self.zlib.decompress(chunk)
        except Exception:
            raise errors.ContentEncodingError('deflate')

        if chunk:
            self.out.feed_data(chunk, len(chunk))
