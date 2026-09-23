    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def var(self, ddof: int = 1, *args, **kwargs):
        """
        Compute variance of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        Returns
        -------
        Series or DataFrame
            Variance of values within each group.
        """
        nv.validate_groupby_func("var", args, kwargs)
        if ddof == 1:
            return self._cython_agg_general(
                "var", alt=lambda x, axis: Series(x).var(ddof=ddof, **kwargs), **kwargs
            )
        else:
            f = lambda x: x.var(ddof=ddof, **kwargs)
            with _group_selection_context(self):
                return self._python_agg_general(f)
