    def _maybe_encode_stream(self, stream):
        if CONTENT_ENCODING in self.headers:
            stream = self._apply_content_encoding(stream)
        if CONTENT_TRANSFER_ENCODING in self.headers:
            stream = self._apply_content_transfer_encoding(stream)
        yield from stream
