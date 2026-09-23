    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        if self.is_stream_consumed:
            raise StreamConsumed()
        self.is_stream_consumed = True
        async for part in self.aiterator:
            yield part
