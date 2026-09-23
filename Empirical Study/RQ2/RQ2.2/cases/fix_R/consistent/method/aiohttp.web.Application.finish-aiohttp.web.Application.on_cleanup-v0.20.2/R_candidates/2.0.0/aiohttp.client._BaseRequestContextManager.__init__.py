    def __init__(self, coro):
        self._coro = coro
        self._resp = None
        self.send = coro.send
        self.throw = coro.throw
        self.close = coro.close
