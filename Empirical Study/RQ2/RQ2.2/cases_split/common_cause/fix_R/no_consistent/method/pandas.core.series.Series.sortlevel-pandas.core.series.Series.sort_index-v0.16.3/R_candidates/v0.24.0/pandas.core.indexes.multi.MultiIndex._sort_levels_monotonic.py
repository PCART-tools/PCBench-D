    def _sort_levels_monotonic(self):
        """
        .. versionadded:: 0.20.0

        This is an *internal* function.

        Create a new MultiIndex from the current to monotonically sorted
        items IN the levels. This does not actually make the entire MultiIndex
        monotonic, JUST the levels.

        The resulting MultiIndex will have the same outward
        appearance, meaning the same .values and ordering. It will also
        be .equals() to the original.

        Returns
        -------
        MultiIndex

        Examples
        --------

        >>> i = pd.MultiIndex(levels=[['a', 'b'], ['bb', 'aa']],
                              codes=[[0, 0, 1, 1], [0, 1, 0, 1]])
        >>> i
        MultiIndex(levels=[['a', 'b'], ['bb', 'aa']],
                   codes=[[0, 0, 1, 1], [0, 1, 0, 1]])

        >>> i.sort_monotonic()
        MultiIndex(levels=[['a', 'b'], ['aa', 'bb']],
                   codes=[[0, 0, 1, 1], [1, 0, 1, 0]])

        """

        if self.is_lexsorted() and self.is_monotonic:
            return self

        new_levels = []
        new_codes = []

        for lev, level_codes in zip(self.levels, self.codes):

            if not lev.is_monotonic:
                try:
                    # indexer to reorder the levels
                    indexer = lev.argsort()
                except TypeError:
                    pass
                else:
                    lev = lev.take(indexer)

                    # indexer to reorder the level codes
                    indexer = ensure_int64(indexer)
                    ri = lib.get_reverse_indexer(indexer, len(indexer))
                    level_codes = algos.take_1d(ri, level_codes)

            new_levels.append(lev)
            new_codes.append(level_codes)

        return MultiIndex(new_levels, new_codes,
                          names=self.names, sortorder=self.sortorder,
                          verify_integrity=False)
