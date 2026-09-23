    @Substitution(name='groupby')
    @Appender(_common_see_also)
    def var(self, ddof=1, *args, **kwargs):
        """
        Compute variance of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : integer, default 1
            degrees of freedom
        """
        nv.validate_groupby_func('var', args, kwargs)
        if ddof == 1:
            try:
                return self._cython_agg_general('var', **kwargs)
            except Exception:
                f = lambda x: x.var(ddof=ddof, **kwargs)
                with _group_selection_context(self):
                    return self._python_agg_general(f)
        else:
            f = lambda x: x.var(ddof=ddof, **kwargs)
            with _group_selection_context(self):
                return self._python_agg_general(f)
