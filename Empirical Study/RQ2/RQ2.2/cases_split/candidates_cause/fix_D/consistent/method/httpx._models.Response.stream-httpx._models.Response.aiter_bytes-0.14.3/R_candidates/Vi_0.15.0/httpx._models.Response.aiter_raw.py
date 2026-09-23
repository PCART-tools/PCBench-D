    async def aiter_raw(self) -> typing.AsyncIterator[bytes]:
        """
        A byte-iterator over the raw response content.
        """
        if self.is_stream_consumed:
            raise StreamConsumed()
        if self.is_closed:
            raise ResponseClosed()
        if not isinstance(self.stream, typing.AsyncIterable):
            raise RuntimeError("Attempted to call a async iterator on a sync stream.")

        self.is_stream_consumed = True
        self._num_bytes_downloaded = 0
        with map_exceptions(HTTPCORE_EXC_MAP, request=self._request):
            async for part in self.stream:
                self._num_bytes_downloaded += len(part)
                yield part
        await self.aclose()
