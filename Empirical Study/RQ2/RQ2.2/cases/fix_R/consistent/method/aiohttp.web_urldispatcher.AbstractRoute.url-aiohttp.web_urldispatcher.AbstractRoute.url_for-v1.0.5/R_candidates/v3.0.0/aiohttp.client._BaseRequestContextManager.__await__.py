    def __await__(self):
        ret = self._coro.__await__()
        return ret
