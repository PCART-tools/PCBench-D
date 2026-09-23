    def send(self, arg):
        self._awaited = True
        return self._coro.send(arg)
