    def __call__(self):
        """Return the current element, or None."""
        return self._elements[self._pos] if self._elements else None
