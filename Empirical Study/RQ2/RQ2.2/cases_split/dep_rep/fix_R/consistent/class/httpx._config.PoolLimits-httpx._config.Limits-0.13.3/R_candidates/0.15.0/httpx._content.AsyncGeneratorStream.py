class AsyncGeneratorStream:
    """
    Request content encoded as plain bytes, using an async byte iterator.
    """

    def __init__(self, agenerator: AsyncIterable[bytes]) -> None:
        self._agenerator = agenerator
        self._is_stream_consumed = False

    async def __aiter__(self) -> AsyncIterator[bytes]:
        if self._is_stream_consumed:
            raise StreamConsumed()

        self._is_stream_consumed = True
        async for part in self._agenerator:
            yield part
