    def back(self):
        """Move the position back and return the current element."""
        self._pos = max(self._pos - 1, 0)
        return self()
