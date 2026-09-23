    def __iter__(self):
        yield from self._dict
        for k, v in self._pairs:
            yield k
