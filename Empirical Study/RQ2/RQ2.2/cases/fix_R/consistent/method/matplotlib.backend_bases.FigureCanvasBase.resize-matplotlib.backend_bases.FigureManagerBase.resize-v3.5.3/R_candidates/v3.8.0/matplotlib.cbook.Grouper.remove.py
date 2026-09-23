    def remove(self, a):
        """Remove *a* from the grouper, doing nothing if it is not there."""
        set_a = self._mapping.pop(a, None)
        if set_a:
            set_a.remove(a)
