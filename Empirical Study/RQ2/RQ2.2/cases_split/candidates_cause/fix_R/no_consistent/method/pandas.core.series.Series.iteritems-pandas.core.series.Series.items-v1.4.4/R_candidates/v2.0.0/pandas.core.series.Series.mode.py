    def mode(self, dropna: bool = True) -> Series:
        """
        Return the mode(s) of the Series.

        The mode is the value that appears most often. There can be multiple modes.

        Always returns Series even if only one value is returned.

        Parameters
        ----------
        dropna : bool, default True
            Don't consider counts of NaN/NaT.

        Returns
        -------
        Series
            Modes of the Series in sorted order.
        """
        # TODO: Add option for bins like value_counts()
        values = self._values
        if isinstance(values, np.ndarray):
            res_values = algorithms.mode(values, dropna=dropna)
        else:
            res_values = values._mode(dropna=dropna)

        # Ensure index is type stable (should always use int index)
        return self._constructor(
            res_values, index=range(len(res_values)), name=self.name, copy=False
        )
