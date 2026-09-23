    def rank(self, method='average', na_option='keep', ascending=True):
        """
        Compute data ranks (1 through n). Equal values are assigned a rank that
        is the average of the ranks of those values

        Parameters
        ----------
        method : {'average', 'min', 'max', 'first'}
            average: average rank of group
            min: lowest rank in group
            max: highest rank in group
            first: ranks assigned in order they appear in the array
        na_option : {'keep'}
            keep: leave NA values where they are
        ascending : boolean, default True
            False for ranks by high (1) to low (N)

        Returns
        -------
        ranks : Series
        """
        from pandas.core.algorithms import rank
        ranks = rank(self.values, method=method, na_option=na_option,
                     ascending=ascending)
        return self._constructor(ranks, index=self.index).__finalize__(self)
