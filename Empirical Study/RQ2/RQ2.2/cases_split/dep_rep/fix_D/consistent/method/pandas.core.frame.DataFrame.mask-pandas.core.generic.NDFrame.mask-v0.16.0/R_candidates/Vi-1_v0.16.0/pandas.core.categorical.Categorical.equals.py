    def equals(self, other):
        """
        Returns True if categorical arrays are equal.

        The name of the `Categorical` is not compared!

        Parameters
        ----------
        other : `Categorical`

        Returns
        -------
        are_equal : boolean
        """
        if not isinstance(other, Categorical):
            return False
        # TODO: should this also test if name is equal?
        return (self.categories.equals(other.categories) and self.ordered == other.ordered and
                np.array_equal(self._codes, other._codes))
