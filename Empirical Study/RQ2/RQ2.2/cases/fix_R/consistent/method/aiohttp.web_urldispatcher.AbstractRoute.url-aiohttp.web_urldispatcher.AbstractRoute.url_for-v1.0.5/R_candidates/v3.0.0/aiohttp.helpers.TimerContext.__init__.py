    def __init__(self, loop):
        self._loop = loop
        self._tasks = []
        self._cancelled = False
