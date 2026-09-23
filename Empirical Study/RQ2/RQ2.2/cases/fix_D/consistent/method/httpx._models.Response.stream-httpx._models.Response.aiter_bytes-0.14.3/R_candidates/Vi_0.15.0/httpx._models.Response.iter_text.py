    def iter_text(self) -> typing.Iterator[str]:
        """
        A str-iterator over the decoded response content
        that handles both gzip, deflate, etc but also detects the content's
        string encoding.
        """
        decoder = TextDecoder(encoding=self.encoding)
        with self._wrap_decoder_errors():
            for chunk in self.iter_bytes():
                yield decoder.decode(chunk)
            yield decoder.flush()
