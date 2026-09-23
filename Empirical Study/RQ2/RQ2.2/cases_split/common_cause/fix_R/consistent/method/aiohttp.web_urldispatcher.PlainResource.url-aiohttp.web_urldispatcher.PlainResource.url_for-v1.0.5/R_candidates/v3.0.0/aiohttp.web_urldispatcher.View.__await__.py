    def __await__(self):
        return self._iter().__await__()
