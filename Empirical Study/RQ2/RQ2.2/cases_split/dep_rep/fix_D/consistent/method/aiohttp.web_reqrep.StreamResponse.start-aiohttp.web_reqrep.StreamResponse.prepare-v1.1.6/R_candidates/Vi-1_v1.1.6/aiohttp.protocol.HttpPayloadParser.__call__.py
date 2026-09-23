    def __call__(self, out, buf):
        # payload params
        length = self.message.headers.get(hdrs.CONTENT_LENGTH, self.length)
        if hdrs.SEC_WEBSOCKET_KEY1 in self.message.headers:
            length = 8

        # payload decompression wrapper
        if (self.response_with_body and
                self.compression and self.message.compression):
            out = DeflateBuffer(out, self.message.compression)

        # payload parser
        if not self.response_with_body:
            # don't parse payload if it's not expected to be received
            pass

        elif 'chunked' in self.message.headers.get(
                hdrs.TRANSFER_ENCODING, ''):
            yield from self.parse_chunked_payload(out, buf)

        elif length is not None:
            try:
                length = int(length)
            except ValueError:
                raise errors.InvalidHeader(hdrs.CONTENT_LENGTH) from None

            if length < 0:
                raise errors.InvalidHeader(hdrs.CONTENT_LENGTH)
            elif length > 0:
                yield from self.parse_length_payload(out, buf, length)
        else:
            if self.readall and getattr(self.message, 'code', 0) != 204:
                yield from self.parse_eof_payload(out, buf)
            elif getattr(self.message, 'method', None) in ('PUT', 'POST'):
                internal_logger.warning(  # pragma: no cover
                    'Content-Length or Transfer-Encoding header is required')

        out.feed_eof()
