    def __getstate__(self) -> bytes:
        return self._ldf.__getstate__()
