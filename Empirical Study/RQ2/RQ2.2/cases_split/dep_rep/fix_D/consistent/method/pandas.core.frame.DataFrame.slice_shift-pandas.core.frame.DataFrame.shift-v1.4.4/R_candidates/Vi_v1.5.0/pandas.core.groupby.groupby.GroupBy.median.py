    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def median(self, numeric_only: bool | lib.NoDefault = lib.no_default):
        """
        Compute median of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex

        Parameters
        ----------
        numeric_only : bool, default True
            Include only float, int, boolean columns. If None, will attempt to use
            everything, then use only numeric data.

        Returns
        -------
        Series or DataFrame
            Median of values within each group.
        """
        numeric_only_bool = self._resolve_numeric_only("median", numeric_only, axis=0)

        result = self._cython_agg_general(
            "median",
            alt=lambda x: Series(x).median(numeric_only=numeric_only_bool),
            numeric_only=numeric_only,
        )
        return result.__finalize__(self.obj, method="groupby")
