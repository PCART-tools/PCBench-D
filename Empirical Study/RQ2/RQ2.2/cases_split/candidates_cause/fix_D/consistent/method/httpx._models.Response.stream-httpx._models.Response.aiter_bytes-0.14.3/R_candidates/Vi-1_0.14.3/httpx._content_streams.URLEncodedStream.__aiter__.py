    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        yield self.body
