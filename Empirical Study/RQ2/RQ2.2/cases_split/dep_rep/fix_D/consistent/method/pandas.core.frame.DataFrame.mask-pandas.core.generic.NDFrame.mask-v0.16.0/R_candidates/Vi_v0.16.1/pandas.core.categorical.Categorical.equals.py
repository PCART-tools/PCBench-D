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
        # TODO: should this also test if name is equal?
        return self.is_dtype_equal(other) and np.array_equal(self._codes, other._codes)
