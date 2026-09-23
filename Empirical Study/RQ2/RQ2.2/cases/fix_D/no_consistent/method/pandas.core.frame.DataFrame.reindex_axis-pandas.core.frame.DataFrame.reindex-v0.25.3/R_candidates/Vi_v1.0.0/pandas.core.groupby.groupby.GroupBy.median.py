    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def median(self, **kwargs):
        """
        Compute median of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex

        Returns
        -------
        Series or DataFrame
            Median of values within each group.
        """
        return self._cython_agg_general(
            "median",
            alt=lambda x, axis: Series(x).median(axis=axis, **kwargs),
            **kwargs,
        )
