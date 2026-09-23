    def __call__(self):
        """Return the current element, or None."""
        if not len(self._elements):
            return self._default
        else:
            return self._elements[self._pos]
