    def sortlevel(
        self,
        level: IndexLabel = 0,
        ascending: bool | list[bool] = True,
        sort_remaining: bool = True,
        na_position: str = "first",
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
        na_position : {'first' or 'last'}, default 'first'
            Argument 'first' puts NaNs at the beginning, 'last' puts NaNs at
            the end.

            .. versionadded:: 2.1.0

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
        if not is_list_like(level):
            level = [level]
        # error: Item "Hashable" of "Union[Hashable, Sequence[Hashable]]" has
        # no attribute "__iter__" (not iterable)
        level = [
            self._get_level_number(lev) for lev in level  # type: ignore[union-attr]
        ]
        sortorder = None

        codes = [self.codes[lev] for lev in level]
        # we have a directed ordering via ascending
        if isinstance(ascending, list):
            if not len(level) == len(ascending):
                raise ValueError("level must have same length as ascending")
        elif sort_remaining:
            codes.extend(
                [self.codes[lev] for lev in range(len(self.levels)) if lev not in level]
            )
        else:
            sortorder = level[0]

        indexer = lexsort_indexer(
            codes, orders=ascending, na_position=na_position, codes_given=True
        )

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
