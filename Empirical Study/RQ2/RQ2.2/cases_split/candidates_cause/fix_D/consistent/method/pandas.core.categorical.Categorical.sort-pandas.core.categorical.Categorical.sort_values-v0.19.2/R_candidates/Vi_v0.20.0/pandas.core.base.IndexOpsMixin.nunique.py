    def nunique(self, dropna=True):
        """
        Return number of unique elements in the object.

        Excludes NA values by default.

        Parameters
        ----------
        dropna : boolean, default True
            Don't include NaN in the count.

        Returns
        -------
        nunique : int
        """
        uniqs = self.unique()
        n = len(uniqs)
        if dropna and isnull(uniqs).any():
            n -= 1
        return n
