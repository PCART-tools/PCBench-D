    def _ixs(self, i: int, axis: AxisInt = 0) -> Any:
        """
        Return the i-th value or values in the Series by location.

        Parameters
        ----------
        i : int

        Returns
        -------
        scalar (int) or Series (slice, sequence)
        """
        return self._values[i]
