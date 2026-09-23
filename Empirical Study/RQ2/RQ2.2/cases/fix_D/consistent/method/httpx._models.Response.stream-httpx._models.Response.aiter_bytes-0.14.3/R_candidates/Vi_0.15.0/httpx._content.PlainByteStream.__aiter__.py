    async def __aiter__(self) -> AsyncIterator[bytes]:
        yield self._body
