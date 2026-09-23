    def iter_bytes(self) -> typing.Iterator[bytes]:
        """
        A byte-iterator over the decoded response content.
        This allows us to handle gzip, deflate, and brotli encoded responses.
        """
        if hasattr(self, "_content"):
            yield self._content
        else:
            decoder = self._get_content_decoder()
            with self._wrap_decoder_errors():
                for chunk in self.iter_raw():
                    yield decoder.decode(chunk)
                yield decoder.flush()
