    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def std(self, ddof=1, *args, **kwargs):
        """
        Compute standard deviation of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : integer, default 1
            degrees of freedom

        Returns
        -------
        Series or DataFrame
            Standard deviation of values within each group.
        """

        # TODO: implement at Cython level?
        nv.validate_groupby_func("std", args, kwargs)
        return np.sqrt(self.var(ddof=ddof, **kwargs))
