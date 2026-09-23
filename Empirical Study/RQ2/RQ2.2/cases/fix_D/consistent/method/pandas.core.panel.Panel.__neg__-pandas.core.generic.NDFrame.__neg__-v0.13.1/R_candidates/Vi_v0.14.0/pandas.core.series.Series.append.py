    def append(self, to_append, verify_integrity=False):
        """
        Concatenate two or more Series. The indexes must not overlap

        Parameters
        ----------
        to_append : Series or list/tuple of Series
        verify_integrity : boolean, default False
            If True, raise Exception on creating index with duplicates

        Returns
        -------
        appended : Series
        """
        from pandas.tools.merge import concat

        if isinstance(to_append, (list, tuple)):
            to_concat = [self] + to_append
        else:
            to_concat = [self, to_append]
        return concat(to_concat, ignore_index=False,
                      verify_integrity=verify_integrity)
