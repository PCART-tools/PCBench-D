class PlainByteStream:
    """
    Request content encoded as plain bytes.
    """

    def __init__(self, body: bytes) -> None:
        self._body = body

    def __iter__(self) -> Iterator[bytes]:
        yield self._body

    async def __aiter__(self) -> AsyncIterator[bytes]:
        yield self._body
