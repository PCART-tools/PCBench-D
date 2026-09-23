    def sortlevel(self, level=0, ascending=True, sort_remaining=True):
        """
        DEPRECATED: use :meth:`Series.sort_index`

        Sort Series with MultiIndex by chosen level. Data will be
        lexicographically sorted by the chosen level followed by the other
        levels (in order)

        Parameters
        ----------
        level : int or level name, default None
        ascending : bool, default True

        Returns
        -------
        sorted : Series

        See Also
        --------
        Series.sort_index(level=...)

        """
        warnings.warn("sortlevel is deprecated, use sort_index(level=...)",
                      FutureWarning, stacklevel=2)
        return self.sort_index(level=level, ascending=ascending,
                               sort_remaining=sort_remaining)
