    def __iter__(self):
        self._do_expiration()
        for val in self._cookies.values():
            yield from val.values()
