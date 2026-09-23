    def __init__(self, loop, timeout):
        self._timeout = timeout
        self._loop = loop
        self._callbacks = []
