    def feed_data(self, chunk, size):
        self.size += size
        try:
            chunk = self.decompressor.decompress(chunk)
        except Exception:
            if not self._started_decoding and self.encoding == 'deflate':
                self.decompressor = zlib.decompressobj()
                try:
                    chunk = self.decompressor.decompress(chunk)
                except Exception:
                    raise ContentEncodingError(
                        'Can not decode content-encoding: %s' % self.encoding)
            else:
                raise ContentEncodingError(
                    'Can not decode content-encoding: %s' % self.encoding)

        if chunk:
            self._started_decoding = True
            self.out.feed_data(chunk, len(chunk))
