    def isin(self, values) -> np.ndarray:
        """
        Pointwise comparison for set containment in the given values.

        Roughly equivalent to `np.array([x in values for x in self])`

        Parameters
        ----------
        values : Sequence

        Returns
        -------
        np.ndarray[bool]
        """
        return isin(np.asarray(self), values)
