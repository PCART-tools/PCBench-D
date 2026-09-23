class FlowControlDataQueue(DataQueue):
    """FlowControlDataQueue resumes and pauses an underlying stream.

    It is a destination for parsed data."""

    def __init__(self, stream, *, loop=None):
        super().__init__(loop=loop)

        self._stream = stream

    @asyncio.coroutine
    def read(self):
        self._stream.resume_stream()
        try:
            return (yield from super().read())
        finally:
            self._stream.pause_stream()
