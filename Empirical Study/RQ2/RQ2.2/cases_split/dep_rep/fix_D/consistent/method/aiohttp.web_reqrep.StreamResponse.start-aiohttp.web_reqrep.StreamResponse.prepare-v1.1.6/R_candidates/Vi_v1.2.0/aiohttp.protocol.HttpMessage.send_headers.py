    def send_headers(self, _sep=': ', _end='\r\n'):
        """Writes headers to a stream. Constructs payload writer."""
        # Chunked response is only for HTTP/1.1 clients or newer
        # and there is no Content-Length header is set.
        # Do not use chunked responses when the response is guaranteed to
        # not have a response body (304, 204).
        assert not self.headers_sent, 'headers have been sent already'
        self.headers_sent = True

        if self.chunked or self.autochunked():
            self.writer = self._write_chunked_payload()
            self.headers[hdrs.TRANSFER_ENCODING] = 'chunked'

        elif self.length is not None:
            self.writer = self._write_length_payload(self.length)

        else:
            self.writer = self._write_eof_payload()

        next(self.writer)

        self._add_default_headers()

        # status + headers
        headers = self.status_line + ''.join(
            [k + _sep + v + _end for k, v in self.headers.items()])
        headers = headers.encode('utf-8') + b'\r\n'

        self.output_length += len(headers)
        self.headers_length = len(headers)
        self.transport.write(headers)
