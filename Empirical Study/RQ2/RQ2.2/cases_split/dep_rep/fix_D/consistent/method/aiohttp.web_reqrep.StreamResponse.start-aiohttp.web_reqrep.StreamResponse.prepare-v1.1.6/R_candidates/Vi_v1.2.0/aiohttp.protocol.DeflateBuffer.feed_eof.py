    def feed_eof(self):
        chunk = self.zlib.flush()
        self.out.feed_data(chunk, len(chunk))
        if not self.zlib.eof:
            raise errors.ContentEncodingError('deflate')

        self.out.feed_eof()
