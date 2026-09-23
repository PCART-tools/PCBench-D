    def sortlevel(self, level=None, ascending=True, sort_remaining=None):
        """
        For internal compatibility with with the Index API.

        Sort the Index. This is for compat with MultiIndex

        Parameters
        ----------
        ascending : boolean, default True
            False to sort in descending order

        level, sort_remaining are compat parameters

        Returns
        -------
        Index
        """
        return self.sort_values(return_indexer=True, ascending=ascending)
