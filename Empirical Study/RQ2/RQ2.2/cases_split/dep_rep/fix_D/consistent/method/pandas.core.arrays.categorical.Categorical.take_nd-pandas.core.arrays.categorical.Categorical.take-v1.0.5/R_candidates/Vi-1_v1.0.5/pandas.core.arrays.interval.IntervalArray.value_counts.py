    def value_counts(self, dropna=True):
        """
        Returns a Series containing counts of each interval.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN.

        Returns
        -------
        counts : Series

        See Also
        --------
        Series.value_counts
        """
        # TODO: implement this is a non-naive way!
        return value_counts(np.asarray(self), dropna=dropna)
