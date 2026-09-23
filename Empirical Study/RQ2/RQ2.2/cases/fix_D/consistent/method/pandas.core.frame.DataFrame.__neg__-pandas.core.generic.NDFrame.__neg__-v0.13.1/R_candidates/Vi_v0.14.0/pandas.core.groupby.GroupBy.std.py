    def std(self, ddof=1):
        """
        Compute standard deviation of groups, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        # todo, implement at cython level?
        if ddof == 1:
            return self._cython_agg_general('std')
        else:
            self._set_selection_from_grouper()
            f = lambda x: x.std(ddof=ddof)
            return self._python_agg_general(f)
