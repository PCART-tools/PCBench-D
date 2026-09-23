    def mode(self):
        """Returns the mode(s) of the dataset.

        Empty if nothing occurs at least 2 times.  Always returns Series even
        if only one value.

        Parameters
        ----------
        sort : bool, default True
            If True, will lexicographically sort values, if False skips
            sorting. Result ordering when ``sort=False`` is not defined.

        Returns
        -------
        modes : Series (sorted)
        """
        # TODO: Add option for bins like value_counts()
        return algos.mode(self)
