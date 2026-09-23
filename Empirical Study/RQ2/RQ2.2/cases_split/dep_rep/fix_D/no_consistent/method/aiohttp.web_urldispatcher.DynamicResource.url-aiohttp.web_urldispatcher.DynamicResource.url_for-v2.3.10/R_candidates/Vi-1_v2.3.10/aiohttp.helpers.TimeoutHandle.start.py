    def start(self):
        if self._timeout is not None and self._timeout > 0:
            at = ceil(self._loop.time() + self._timeout)
            return self._loop.call_at(at, self.__call__)
