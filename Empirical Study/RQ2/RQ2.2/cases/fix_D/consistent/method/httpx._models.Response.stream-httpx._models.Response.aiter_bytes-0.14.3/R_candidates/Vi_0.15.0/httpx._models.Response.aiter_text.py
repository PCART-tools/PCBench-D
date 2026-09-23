    async def aiter_text(self) -> typing.AsyncIterator[str]:
        """
        A str-iterator over the decoded response content
        that handles both gzip, deflate, etc but also detects the content's
        string encoding.
        """
        decoder = TextDecoder(encoding=self.encoding)
        with self._wrap_decoder_errors():
            async for chunk in self.aiter_bytes():
                yield decoder.decode(chunk)
            yield decoder.flush()
