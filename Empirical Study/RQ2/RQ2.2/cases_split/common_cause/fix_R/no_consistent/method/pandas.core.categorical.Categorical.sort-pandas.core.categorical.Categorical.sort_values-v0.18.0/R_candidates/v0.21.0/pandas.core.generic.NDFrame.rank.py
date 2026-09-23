    def rank(self, axis=0, method='average', numeric_only=None,
             na_option='keep', ascending=True, pct=False):
        """
        Compute numerical data ranks (1 through n) along axis. Equal values are
        assigned a rank that is the average of the ranks of those values

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            index to direct ranking
        method : {'average', 'min', 'max', 'first', 'dense'}
            * average: average rank of group
            * min: lowest rank in group
            * max: highest rank in group
            * first: ranks assigned in order they appear in the array
            * dense: like 'min', but rank always increases by 1 between groups
        numeric_only : boolean, default None
            Include only float, int, boolean data. Valid only for DataFrame or
            Panel objects
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
        ranks : same type as caller
        """
        axis = self._get_axis_number(axis)

        if self.ndim > 2:
            msg = "rank does not make sense when ndim > 2"
            raise NotImplementedError(msg)

        def ranker(data):
            ranks = algos.rank(data.values, axis=axis, method=method,
                               ascending=ascending, na_option=na_option,
                               pct=pct)
            ranks = self._constructor(ranks, **data._construct_axes_dict())
            return ranks.__finalize__(self)

        # if numeric_only is None, and we can't get anything, we try with
        # numeric_only=True
        if numeric_only is None:
            try:
                return ranker(self)
            except TypeError:
                numeric_only = True

        if numeric_only:
            data = self._get_numeric_data()
        else:
            data = self

        return ranker(data)
