    def update_transfer_encoding(self):
        """Analyze transfer-encoding header."""
        te = self.headers.get(hdrs.TRANSFER_ENCODING, '').lower()

        if 'chunked' in te:
            if self.chunked:
                raise ValueError(
                    'chunked can not be set '
                    'if "Transfer-Encoding: chunked" header is set')

        elif self.chunked:
            if hdrs.CONTENT_LENGTH in self.headers:
                raise ValueError(
                    'chunked can not be set '
                    'if Content-Length header is set')

            self.headers[hdrs.TRANSFER_ENCODING] = 'chunked'
        else:
            if hdrs.CONTENT_LENGTH not in self.headers:
                self.headers[hdrs.CONTENT_LENGTH] = str(len(self.body))
