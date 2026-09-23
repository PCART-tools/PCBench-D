        def __await__(self):
            ret = yield from self._coro
            return ret
