class ChunksQueue(DataQueue):
    """Like a :class:`DataQueue`, but for binary chunked data transfer."""

    @asyncio.coroutine
    def read(self):
        try:
            return (yield from super().read())
        except EofStream:
            return EOF_MARKER

    readany = read
