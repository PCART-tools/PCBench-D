    def push(self, o):
        """
        Push *o* to the stack after the current position, and return *o*.

        Discard all later elements.
        """
        self._elements[self._pos + 1:] = [o]
        self._pos = len(self._elements) - 1
        return o
