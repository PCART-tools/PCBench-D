    def mode(self, dropna=True):
        """
        Return the mode(s) of the dataset.

        Always returns Series even if only one value is returned.

        Parameters
        ----------
        dropna : bool, default True
            Don't consider counts of NaN/NaT.

            .. versionadded:: 0.24.0

        Returns
        -------
        Series
            Modes of the Series in sorted order.
        """
        # TODO: Add option for bins like value_counts()
        return algorithms.mode(self, dropna=dropna)
