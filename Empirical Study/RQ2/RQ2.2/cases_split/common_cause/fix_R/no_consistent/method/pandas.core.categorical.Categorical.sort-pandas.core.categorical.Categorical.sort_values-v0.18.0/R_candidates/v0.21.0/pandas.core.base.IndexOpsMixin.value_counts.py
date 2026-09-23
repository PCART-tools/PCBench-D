    def value_counts(self, normalize=False, sort=True, ascending=False,
                     bins=None, dropna=True):
        """
        Returns object containing counts of unique values.

        The resulting object will be in descending order so that the
        first element is the most frequently-occurring element.
        Excludes NA values by default.

        Parameters
        ----------
        normalize : boolean, default False
            If True then the object returned will contain the relative
            frequencies of the unique values.
        sort : boolean, default True
            Sort by values
        ascending : boolean, default False
            Sort in ascending order
        bins : integer, optional
            Rather than count values, group them into half-open bins,
            a convenience for pd.cut, only works with numeric data
        dropna : boolean, default True
            Don't include counts of NaN.

        Returns
        -------
        counts : Series
        """
        from pandas.core.algorithms import value_counts
        result = value_counts(self, sort=sort, ascending=ascending,
                              normalize=normalize, bins=bins, dropna=dropna)
        return result
