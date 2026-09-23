    def sortlevel(
        self, level=0, ascending: bool = True, sort_remaining: bool = True
    ) -> tuple[MultiIndex, npt.NDArray[np.intp]]:
        """
        Sort MultiIndex at the requested level.

        The result will respect the original ordering of the associated
        factor at that level.

        Parameters
        ----------
        level : list-like, int or str, default 0
            If a string is given, must be a name of the level.
            If list-like must be names or ints of levels.
        ascending : bool, default True
            False to sort in descending order.
            Can also be a list to specify a directed ordering.
        sort_remaining : sort by the remaining levels after level

        Returns
        -------
        sorted_index : pd.MultiIndex
            Resulting index.
        indexer : np.ndarray[np.intp]
            Indices of output values in original index.

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([[0, 0], [2, 1]])
        >>> mi
        MultiIndex([(0, 2),
                    (0, 1)],
                   )

        >>> mi.sortlevel()
        (MultiIndex([(0, 1),
                    (0, 2)],
                   ), array([1, 0]))

        >>> mi.sortlevel(sort_remaining=False)
        (MultiIndex([(0, 2),
                    (0, 1)],
                   ), array([0, 1]))

        >>> mi.sortlevel(1)
        (MultiIndex([(0, 1),
                    (0, 2)],
                   ), array([1, 0]))

        >>> mi.sortlevel(1, ascending=False)
        (MultiIndex([(0, 2),
                    (0, 1)],
                   ), array([0, 1]))
        """
        if isinstance(level, (str, int)):
            level = [level]
        level = [self._get_level_number(lev) for lev in level]
        sortorder = None

        # we have a directed ordering via ascending
        if isinstance(ascending, list):
            if not len(level) == len(ascending):
                raise ValueError("level must have same length as ascending")

            indexer = lexsort_indexer(
                [self.codes[lev] for lev in level], orders=ascending
            )

        # level ordering
        else:

            codes = list(self.codes)
            shape = list(self.levshape)

            # partition codes and shape
            primary = tuple(codes[lev] for lev in level)
            primshp = tuple(shape[lev] for lev in level)

            # Reverse sorted to retain the order of
            # smaller indices that needs to be removed
            for lev in sorted(level, reverse=True):
                codes.pop(lev)
                shape.pop(lev)

            if sort_remaining:
                primary += primary + tuple(codes)
                primshp += primshp + tuple(shape)
            else:
                sortorder = level[0]

            indexer = indexer_from_factorized(primary, primshp, compress=False)

            if not ascending:
                indexer = indexer[::-1]

        indexer = ensure_platform_int(indexer)
        new_codes = [level_codes.take(indexer) for level_codes in self.codes]

        new_index = MultiIndex(
            codes=new_codes,
            levels=self.levels,
            names=self.names,
            sortorder=sortorder,
            verify_integrity=False,
        )

        return new_index, indexer
