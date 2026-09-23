    def difference(self, other) -> "FrozenList":
        """
        Returns a FrozenList with elements from other removed from self.

        Parameters
        ----------
        other : array-like
            The array-like whose elements we are removing self.

        Returns
        -------
        FrozenList
            The collection difference between self and other.
        """
        other = set(other)
        temp = [x for x in self if x not in other]
        return type(self)(temp)
