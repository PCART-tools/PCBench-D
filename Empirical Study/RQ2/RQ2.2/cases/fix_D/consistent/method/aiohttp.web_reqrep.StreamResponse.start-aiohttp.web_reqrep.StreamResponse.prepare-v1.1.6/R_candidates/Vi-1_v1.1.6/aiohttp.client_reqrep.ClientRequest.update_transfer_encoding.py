    def update_transfer_encoding(self):
        """Analyze transfer-encoding header."""
        te = self.headers.get(hdrs.TRANSFER_ENCODING, '').lower()

        if self.chunked:
            if hdrs.CONTENT_LENGTH in self.headers:
                del self.headers[hdrs.CONTENT_LENGTH]
            if 'chunked' not in te:
                self.headers[hdrs.TRANSFER_ENCODING] = 'chunked'

            self.chunked = self.chunked if type(self.chunked) is int else 8192
        else:
            if 'chunked' in te:
                self.chunked = 8192
            else:
                self.chunked = None
                if hdrs.CONTENT_LENGTH not in self.headers:
                    self.headers[hdrs.CONTENT_LENGTH] = str(len(self.body))
