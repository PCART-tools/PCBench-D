    async def aiter_bytes(self) -> typing.AsyncIterator[bytes]:
        """
        A byte-iterator over the decoded response content.
        This allows us to handle gzip, deflate, and brotli encoded responses.
        """
        if hasattr(self, "_content"):
            yield self._content
        else:
            decoder = self._get_content_decoder()
            with self._wrap_decoder_errors():
                async for chunk in self.aiter_raw():
                    yield decoder.decode(chunk)
                yield decoder.flush()
