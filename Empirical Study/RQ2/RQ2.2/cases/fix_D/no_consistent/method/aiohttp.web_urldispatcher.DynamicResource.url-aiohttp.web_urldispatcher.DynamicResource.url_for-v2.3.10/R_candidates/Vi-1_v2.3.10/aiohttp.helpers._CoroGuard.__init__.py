    def __init__(self, coro, msg):
        super().__init__(coro)
        self._msg = msg
        self._awaited = False
