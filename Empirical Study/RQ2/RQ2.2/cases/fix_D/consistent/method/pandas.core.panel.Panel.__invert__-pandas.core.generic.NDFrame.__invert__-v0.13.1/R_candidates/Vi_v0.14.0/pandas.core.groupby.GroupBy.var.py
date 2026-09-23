    def var(self, ddof=1):
        """
        Compute variance of groups, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        if ddof == 1:
            return self._cython_agg_general('var')
        else:
            self._set_selection_from_grouper()
            f = lambda x: x.var(ddof=ddof)
            return self._python_agg_general(f)
