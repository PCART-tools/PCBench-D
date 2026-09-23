    def get_siblings(self, a):
        """Return all of the items joined with *a*, including itself."""
        siblings = self._mapping.get(a, [a])
        return sorted(siblings, key=self._ordering.get)
