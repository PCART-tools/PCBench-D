    def rank(self, method='average', na_option='keep', ascending=True,
             pct=False):
        """
        Compute data ranks (1 through n). Equal values are assigned a rank that
        is the average of the ranks of those values

        Parameters
        ----------
        method : {'average', 'min', 'max', 'first', 'dense'}
            * average: average rank of group
            * min: lowest rank in group
            * max: highest rank in group
            * first: ranks assigned in order they appear in the array
            * dense: like 'min', but rank always increases by 1 between groups
        na_option : {'keep'}
            keep: leave NA values where they are
        ascending : boolean, default True
            False for ranks by high (1) to low (N)
        pct : boolean, default False
            Computes percentage rank of data

        Returns
        -------
        ranks : Series
        """
        from pandas.core.algorithms import rank
        ranks = rank(self.values, method=method, na_option=na_option,
                     ascending=ascending, pct=pct)
        return self._constructor(ranks, index=self.index).__finalize__(self)
