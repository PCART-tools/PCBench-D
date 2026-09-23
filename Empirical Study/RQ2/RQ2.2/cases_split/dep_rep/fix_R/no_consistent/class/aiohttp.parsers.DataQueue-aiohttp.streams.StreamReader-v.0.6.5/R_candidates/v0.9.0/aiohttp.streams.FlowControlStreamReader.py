class FlowControlStreamReader(StreamReader):

    def __init__(self, stream, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._stream = stream

    @asyncio.coroutine
    def read(self, n=-1):
        self._stream.resume_stream()
        try:
            return (yield from super().read(n))
        finally:
            self._stream.pause_stream()

    @asyncio.coroutine
    def readline(self):
        self._stream.resume_stream()
        try:
            return (yield from super().readline())
        finally:
            self._stream.pause_stream()

    @asyncio.coroutine
    def readany(self):
        self._stream.resume_stream()
        try:
            return (yield from super().readany())
        finally:
            self._stream.pause_stream()

    @asyncio.coroutine
    def readexactly(self, n):
        self._stream.resume_stream()
        try:
            return (yield from super().readexactly(n))
        finally:
            self._stream.pause_stream()
