    @Substitution(name='groupby')
    @Appender(_doc_template)
    def rank(self, method='average', ascending=True, na_option='keep',
             pct=False, axis=0):
        """
        Provides the rank of values within each group.

        Parameters
        ----------
        method : {'average', 'min', 'max', 'first', 'dense'}, default 'average'
            * average: average rank of group
            * min: lowest rank in group
            * max: highest rank in group
            * first: ranks assigned in order they appear in the array
            * dense: like 'min', but rank always increases by 1 between groups
        ascending : boolean, default True
            False for ranks by high (1) to low (N)
        na_option :  {'keep', 'top', 'bottom'}, default 'keep'
            * keep: leave NA values where they are
            * top: smallest rank if ascending
            * bottom: smallest rank if descending
        pct : boolean, default False
            Compute percentage rank of data within each group
        axis : int, default 0
            The axis of the object over which to compute the rank.

        Returns
        -----
        DataFrame with ranking of values within each group
        """
        return self._cython_transform('rank', numeric_only=False,
                                      ties_method=method, ascending=ascending,
                                      na_option=na_option, pct=pct, axis=axis)
