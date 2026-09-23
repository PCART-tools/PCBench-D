    def mode(self, dropna=True):
        """
        Return the mode(s) of the dataset.

        Always returns Series even if only one value is returned.

        Parameters
        ----------
        dropna : boolean, default True
            Don't consider counts of NaN/NaT.

            .. versionadded:: 0.24.0

        Returns
        -------
        modes : Series (sorted)
        """
        # TODO: Add option for bins like value_counts()
        return algorithms.mode(self, dropna=dropna)
