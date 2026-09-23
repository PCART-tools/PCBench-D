    def joined(self, a, b):
        """Return whether *a* and *b* are members of the same set."""
        return (self._mapping.get(a, object()) is self._mapping.get(b))
