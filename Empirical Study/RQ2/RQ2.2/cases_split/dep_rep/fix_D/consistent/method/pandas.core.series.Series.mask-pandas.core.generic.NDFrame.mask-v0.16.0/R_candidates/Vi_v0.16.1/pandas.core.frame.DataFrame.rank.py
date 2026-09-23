    def rank(self, axis=0, numeric_only=None, method='average',
             na_option='keep', ascending=True, pct=False):
        """
        Compute numerical data ranks (1 through n) along axis. Equal values are
        assigned a rank that is the average of the ranks of those values

        Parameters
        ----------
        axis : {0, 1}, default 0
            Ranks over columns (0) or rows (1)
        numeric_only : boolean, default None
            Include only float, int, boolean data
        method : {'average', 'min', 'max', 'first', 'dense'}
            * average: average rank of group
            * min: lowest rank in group
            * max: highest rank in group
            * first: ranks assigned in order they appear in the array
            * dense: like 'min', but rank always increases by 1 between groups
        na_option : {'keep', 'top', 'bottom'}
            * keep: leave NA values where they are
            * top: smallest rank if ascending
            * bottom: smallest rank if descending
        ascending : boolean, default True
            False for ranks by high (1) to low (N)
        pct : boolean, default False
            Computes percentage rank of data

        Returns
        -------
        ranks : DataFrame
        """
        axis = self._get_axis_number(axis)
        if numeric_only is None:
            try:
                ranks = algos.rank(self.values, axis=axis, method=method,
                                   ascending=ascending, na_option=na_option,
                                   pct=pct)
                return self._constructor(ranks, index=self.index,
                                         columns=self.columns)
            except TypeError:
                numeric_only = True
        if numeric_only:
            data = self._get_numeric_data()
        else:
            data = self
        ranks = algos.rank(data.values, axis=axis, method=method,
                           ascending=ascending, na_option=na_option, pct=pct)
        return self._constructor(ranks, index=data.index, columns=data.columns)
