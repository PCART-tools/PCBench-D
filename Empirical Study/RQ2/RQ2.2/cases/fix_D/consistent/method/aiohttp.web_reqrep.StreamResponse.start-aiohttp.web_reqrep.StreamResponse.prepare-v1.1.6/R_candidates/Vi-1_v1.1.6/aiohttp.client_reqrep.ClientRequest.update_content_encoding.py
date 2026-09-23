    def update_content_encoding(self, data):
        """Set request content encoding."""
        if not data:
            return

        enc = self.headers.get(hdrs.CONTENT_ENCODING, '').lower()
        if enc:
            if self.compress is not False:
                self.compress = enc
                # enable chunked, no need to deal with length
                self.chunked = True
        elif self.compress:
            if not isinstance(self.compress, str):
                self.compress = 'deflate'
            self.headers[hdrs.CONTENT_ENCODING] = self.compress
            self.chunked = True  # enable chunked, no need to deal with length
