    def union(self, other):
        """
        Returns a FrozenList with other concatenated to the end of self.

        Parameters
        ----------
        other : array-like
            The array-like whose elements we are concatenating.

        Returns
        -------
        diff : FrozenList
            The collection difference between self and other.
        """
        if isinstance(other, tuple):
            other = list(other)
        return type(self)(super(FrozenList, self).__add__(other))
