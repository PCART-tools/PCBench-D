    def current(self):
        """Return the active axes, or None if the stack is empty."""
        return max(self._axes, key=self._axes.__getitem__, default=None)
