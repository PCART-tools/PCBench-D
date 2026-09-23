    def feed_eof(self):
        chunk = self.zlib.flush()

        if chunk or self.size > 0:
            self.out.feed_data(chunk, len(chunk))
            if not self.zlib.eof:
                raise ContentEncodingError('deflate')

        self.out.feed_eof()
