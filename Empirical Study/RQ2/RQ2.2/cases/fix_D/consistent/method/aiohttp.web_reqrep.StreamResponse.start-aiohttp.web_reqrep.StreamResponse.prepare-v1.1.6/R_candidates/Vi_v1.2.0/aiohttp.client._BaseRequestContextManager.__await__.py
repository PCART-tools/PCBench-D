        def __await__(self):
            resp = yield from self._coro
            return resp
