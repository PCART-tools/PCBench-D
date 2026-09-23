    def remove(self, a):
        """Remove *a* from the grouper, doing nothing if it is not there."""
        self._mapping.pop(a, {a}).remove(a)
        self._ordering.pop(a, None)
