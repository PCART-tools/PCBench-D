    def back(self):
        """Move the position back and return the current element."""
        if self._pos > 0:
            self._pos -= 1
        return self()
