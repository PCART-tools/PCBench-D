    def serialize(self):
        """Yields byte chunks for body part."""

        has_encoding = (
            CONTENT_ENCODING in self.headers and
            self.headers[CONTENT_ENCODING] != 'identity' or
            CONTENT_TRANSFER_ENCODING in self.headers
        )
        if has_encoding:
            # since we're following streaming approach which doesn't assumes
            # any intermediate buffers, we cannot calculate real content length
            # with the specified content encoding scheme. So, instead of lying
            # about content length and cause reading issues, we have to strip
            # this information.
            self.headers.pop(CONTENT_LENGTH, None)

        if self.headers:
            yield b'\r\n'.join(
                b': '.join(map(lambda i: i.encode('latin1'), item))
                for item in self.headers.items()
            )
        yield b'\r\n\r\n'
        yield from self._maybe_encode_stream(self._serialize_obj())
        yield b'\r\n'
