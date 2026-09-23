    def _ixs(self, i: int, axis: int = 0):
        """
        Return the i-th value or values in the Series by location.

        Parameters
        ----------
        i : int

        Returns
        -------
        scalar (int) or Series (slice, sequence)
        """

        # dispatch to the values if we need
        values = self._values
        if isinstance(values, np.ndarray):
            return libindex.get_value_at(values, i)
        else:
            return values[i]
