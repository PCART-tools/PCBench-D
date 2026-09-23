    def __init__(self, *, loop=None):
        self._loop = loop
        self._eof = False
        self._waiter = None
        self._exception = None
        self._size = 0
        self._buffer = collections.deque()
