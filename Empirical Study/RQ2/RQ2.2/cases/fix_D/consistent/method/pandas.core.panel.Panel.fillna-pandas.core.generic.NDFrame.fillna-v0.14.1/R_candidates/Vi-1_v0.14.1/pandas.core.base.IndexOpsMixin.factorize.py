    def factorize(self, sort=False, na_sentinel=-1):
        """
        Encode the object as an enumerated type or categorical variable

        Parameters
        ----------
        sort : boolean, default False
            Sort by values
        na_sentinel: int, default -1
            Value to mark "not found"

        Returns
        -------
        labels : the indexer to the original array
        uniques : the unique Index
        """
        from pandas.core.algorithms import factorize
        return factorize(self, sort=sort, na_sentinel=na_sentinel)
