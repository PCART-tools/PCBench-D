    def sortlevel(self, level=None, ascending=True, sort_remaining=None):
        """
        For internal compatibility with the Index API.

        Sort the Index. This is for compat with MultiIndex

        Parameters
        ----------
        ascending : bool, default True
            False to sort in descending order

        level, sort_remaining are compat parameters

        Returns
        -------
        Index
        """
        if not isinstance(ascending, (list, bool)):
            raise TypeError(
                "ascending must be a single bool value or"
                "a list of bool values of length 1"
            )

        if isinstance(ascending, list):
            if len(ascending) != 1:
                raise TypeError("ascending must be a list of bool values of length 1")
            ascending = ascending[0]

        if not isinstance(ascending, bool):
            raise TypeError("ascending must be a bool value")

        return self.sort_values(return_indexer=True, ascending=ascending)
