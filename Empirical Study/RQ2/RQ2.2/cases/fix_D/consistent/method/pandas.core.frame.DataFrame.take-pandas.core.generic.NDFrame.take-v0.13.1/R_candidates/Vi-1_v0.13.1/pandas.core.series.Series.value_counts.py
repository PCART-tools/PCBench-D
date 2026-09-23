    def value_counts(self, normalize=False, sort=True, ascending=False,
                     bins=None):
        """
        Returns Series containing counts of unique values. The resulting Series
        will be in descending order so that the first element is the most
        frequently-occurring element. Excludes NA values

        Parameters
        ----------
        normalize : boolean, default False
            If True then the Series returned will contain the relative
            frequencies of the unique values.
        sort : boolean, default True
            Sort by values
        ascending : boolean, default False
            Sort in ascending order
        bins : integer, optional
            Rather than count values, group them into half-open bins,
            a convenience for pd.cut, only works with numeric data

        Returns
        -------
        counts : Series
        """
        from pandas.core.algorithms import value_counts
        return value_counts(self.values, sort=sort, ascending=ascending,
                            normalize=normalize, bins=bins)
