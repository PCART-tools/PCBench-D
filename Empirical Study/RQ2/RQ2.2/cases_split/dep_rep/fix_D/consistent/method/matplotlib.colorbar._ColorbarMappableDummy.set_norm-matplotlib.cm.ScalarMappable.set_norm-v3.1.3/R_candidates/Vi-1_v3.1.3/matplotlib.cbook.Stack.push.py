    def push(self, o):
        """
        Push *o* to the stack at current position.  Discard all later elements.

        *o* is returned.
        """
        self._elements = self._elements[:self._pos + 1] + [o]
        self._pos = len(self._elements) - 1
        return self()
