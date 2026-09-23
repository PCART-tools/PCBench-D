class StreamProtocol(asyncio.streams.FlowControlMixin, asyncio.Protocol):
    """Helper class to adapt between Protocol and StreamReader."""

    def __init__(self, *, loop=None, **kwargs):
        super().__init__(loop=loop)

        self.transport = None
        self.writer = None
        self.reader = StreamParser(loop=loop, **kwargs)

    def is_connected(self):
        return self.transport is not None

    def connection_made(self, transport):
        self.transport = transport
        self.reader.set_transport(transport)
        self.writer = asyncio.streams.StreamWriter(
            transport, self, self.reader, self._loop)

    def connection_lost(self, exc):
        self.transport = None

        if exc is None:
            self.reader.feed_eof()
        else:
            self.reader.set_exception(exc)

        super().connection_lost(exc)

    def data_received(self, data):
        self.reader.feed_data(data)

    def eof_received(self):
        self.reader.feed_eof()

    def _make_drain_waiter(self):
        if not self._paused:
            return ()
        waiter = self._drain_waiter
        if waiter is None or waiter.cancelled():
            waiter = asyncio.Future(loop=self._loop)
            self._drain_waiter = waiter
        return waiter
