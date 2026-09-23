    def sortlevel(self, level=0, axis=0, ascending=True, inplace=False,
                  sort_remaining=True):
        """Sort multilevel index by chosen axis and primary level. Data will be
        lexicographically sorted by the chosen level followed by the other
        levels (in order).

        .. deprecated:: 0.20.0
            Use :meth:`DataFrame.sort_index`


        Parameters
        ----------
        level : int
        axis : {0 or 'index', 1 or 'columns'}, default 0
        ascending : boolean, default True
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance
        sort_remaining : boolean, default True
            Sort by the other levels too.

        Returns
        -------
        sorted : DataFrame

        See Also
        --------
        DataFrame.sort_index(level=...)

        """
        warnings.warn("sortlevel is deprecated, use sort_index(level= ...)",
                      FutureWarning, stacklevel=2)
        return self.sort_index(level=level, axis=axis, ascending=ascending,
                               inplace=inplace, sort_remaining=sort_remaining)
