class DataQueue:
    """DataQueue is a general-purpose blocking queue with one reader."""

    def __init__(self, *, loop=None):
        self._loop = loop
        self._buffer = collections.deque()
        self._eof = False
        self._waiter = None
        self._exception = None

    def is_eof(self):
        return self._eof

    def at_eof(self):
        return self._eof and not self._buffer

    def exception(self):
        return self._exception

    def set_exception(self, exc):
        self._exception = exc

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.done():
                waiter.set_exception(exc)

    def feed_data(self, data):
        self._buffer.append(data)

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_result(True)

    def feed_eof(self):
        self._eof = True

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_result(False)

    @asyncio.coroutine
    def read(self):
        if not self._buffer and not self._eof:
            if self._exception is not None:
                raise self._exception

            assert not self._waiter
            self._waiter = asyncio.Future(loop=self._loop)
            yield from self._waiter

        if self._buffer:
            return self._buffer.popleft()
        else:
            if self._exception is not None:
                raise self._exception
            else:
                raise EofStream
