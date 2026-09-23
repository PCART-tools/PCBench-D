    def __del__(self):
        self._coro = None
        if not self._awaited:
            warnings.warn(self._msg, DeprecationWarning, stacklevel=2)
