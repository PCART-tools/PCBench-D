    def __getstate__(self) -> bytes:
        return self._pyexpr.__getstate__()
