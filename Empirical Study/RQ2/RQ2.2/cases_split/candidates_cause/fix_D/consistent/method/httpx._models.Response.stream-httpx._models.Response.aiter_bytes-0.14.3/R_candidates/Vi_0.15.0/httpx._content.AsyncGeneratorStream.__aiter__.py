    async def __aiter__(self) -> AsyncIterator[bytes]:
        if self._is_stream_consumed:
            raise StreamConsumed()

        self._is_stream_consumed = True
        async for part in self._agenerator:
            yield part
