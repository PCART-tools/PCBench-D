    async def aiter_bytes(self) -> typing.AsyncIterator[bytes]:
        """
        A byte-iterator over the decoded response content.
        This allows us to handle gzip, deflate, and brotli encoded responses.
        """
        if hasattr(self, "_content"):
            yield self._content
        else:
            with self._wrap_decoder_errors():
                async for chunk in self.aiter_raw():
                    yield self.decoder.decode(chunk)
                yield self.decoder.flush()
