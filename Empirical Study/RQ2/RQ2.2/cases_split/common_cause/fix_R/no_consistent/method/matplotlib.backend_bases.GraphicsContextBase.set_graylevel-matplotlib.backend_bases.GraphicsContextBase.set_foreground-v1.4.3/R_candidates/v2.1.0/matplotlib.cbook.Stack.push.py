    def push(self, o):
        """
        push object onto stack at current position - all elements
        occurring later than the current position are discarded
        """
        self._elements = self._elements[:self._pos + 1]
        self._elements.append(o)
        self._pos = len(self._elements) - 1
        return self()
