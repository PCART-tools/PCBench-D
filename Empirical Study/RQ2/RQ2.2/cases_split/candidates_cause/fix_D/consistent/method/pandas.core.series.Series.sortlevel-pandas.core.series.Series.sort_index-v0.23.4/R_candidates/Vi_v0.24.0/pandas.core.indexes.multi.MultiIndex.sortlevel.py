    def sortlevel(self, level=0, ascending=True, sort_remaining=True):
        """
        Sort MultiIndex at the requested level. The result will respect the
        original ordering of the associated factor at that level.

        Parameters
        ----------
        level : list-like, int or str, default 0
            If a string is given, must be a name of the level
            If list-like must be names or ints of levels.
        ascending : boolean, default True
            False to sort in descending order
            Can also be a list to specify a directed ordering
        sort_remaining : sort by the remaining levels after level

        Returns
        -------
        sorted_index : pd.MultiIndex
            Resulting index
        indexer : np.ndarray
            Indices of output values in original index
        """
        from pandas.core.sorting import indexer_from_factorized

        if isinstance(level, (compat.string_types, int)):
            level = [level]
        level = [self._get_level_number(lev) for lev in level]
        sortorder = None

        # we have a directed ordering via ascending
        if isinstance(ascending, list):
            if not len(level) == len(ascending):
                raise ValueError("level must have same length as ascending")

            from pandas.core.sorting import lexsort_indexer
            indexer = lexsort_indexer([self.codes[lev] for lev in level],
                                      orders=ascending)

        # level ordering
        else:

            codes = list(self.codes)
            shape = list(self.levshape)

            # partition codes and shape
            primary = tuple(codes.pop(lev - i) for i, lev in enumerate(level))
            primshp = tuple(shape.pop(lev - i) for i, lev in enumerate(level))

            if sort_remaining:
                primary += primary + tuple(codes)
                primshp += primshp + tuple(shape)
            else:
                sortorder = level[0]

            indexer = indexer_from_factorized(primary, primshp,
                                              compress=False)

            if not ascending:
                indexer = indexer[::-1]

        indexer = ensure_platform_int(indexer)
        new_codes = [level_codes.take(indexer) for level_codes in self.codes]

        new_index = MultiIndex(codes=new_codes, levels=self.levels,
                               names=self.names, sortorder=sortorder,
                               verify_integrity=False)

        return new_index, indexer
