    def feed_eof(self):
        chunk = self.decompressor.flush()

        if chunk or self.size > 0:
            self.out.feed_data(chunk, len(chunk))
            if self.encoding != 'br' and not self.decompressor.eof:
                raise ContentEncodingError('deflate')

        self.out.feed_eof()
