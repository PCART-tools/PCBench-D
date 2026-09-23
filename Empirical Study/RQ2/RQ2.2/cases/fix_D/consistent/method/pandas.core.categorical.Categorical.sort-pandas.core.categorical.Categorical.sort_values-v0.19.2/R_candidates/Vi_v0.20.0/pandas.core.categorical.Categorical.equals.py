    def equals(self, other):
        """
        Returns True if categorical arrays are equal.

        Parameters
        ----------
        other : `Categorical`

        Returns
        -------
        are_equal : boolean
        """
        return (self.is_dtype_equal(other) and
                np.array_equal(self._codes, other._codes))
