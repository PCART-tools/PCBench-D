    def isin(self, values) -> npt.NDArray[np.bool_]:
        """
        Pointwise comparison for set containment in the given values.

        Roughly equivalent to `np.array([x in values for x in self])`

        Parameters
        ----------
        values : Sequence

        Returns
        -------
        np.ndarray[bool]

        Examples
        --------
        >>> arr = pd.array([1, 2, 3])
        >>> arr.isin([1])
        <BooleanArray>
        [True, False, False]
        Length: 3, dtype: boolean
        """
        return isin(np.asarray(self), values)
