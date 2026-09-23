    def __getstate__(self) -> bytes:
        return self._s.__getstate__()
