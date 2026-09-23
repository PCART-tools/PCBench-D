    def set_levels(self, levels, level=None, inplace=False, verify_integrity=True):
        """
        Set new levels on MultiIndex. Defaults to returning
        new index.

        Parameters
        ----------
        levels : sequence or list of sequence
            new level(s) to apply
        level : int, level name, or sequence of int/level names (default None)
            level(s) to set (None for all levels)
        inplace : bool
            if True, mutates in place
        verify_integrity : bool (default True)
            if True, checks that levels and codes are compatible

        Returns
        -------
        new index (of same type and class...etc)

        Examples
        --------
        >>> idx = pd.MultiIndex.from_tuples([(1, 'one'), (1, 'two'),
                                            (2, 'one'), (2, 'two')],
                                            names=['foo', 'bar'])
        >>> idx.set_levels([['a', 'b'], [1, 2]])
        MultiIndex([('a', 1),
                    ('a', 2),
                    ('b', 1),
                    ('b', 2)],
                   names=['foo', 'bar'])
        >>> idx.set_levels(['a', 'b'], level=0)
        MultiIndex([('a', 'one'),
                    ('a', 'two'),
                    ('b', 'one'),
                    ('b', 'two')],
                   names=['foo', 'bar'])
        >>> idx.set_levels(['a', 'b'], level='bar')
        MultiIndex([(1, 'a'),
                    (1, 'b'),
                    (2, 'a'),
                    (2, 'b')],
                   names=['foo', 'bar'])
        >>> idx.set_levels([['a', 'b'], [1, 2]], level=[0, 1])
        MultiIndex([('a', 1),
                    ('a', 2),
                    ('b', 1),
                    ('b', 2)],
                   names=['foo', 'bar'])
        """
        if is_list_like(levels) and not isinstance(levels, Index):
            levels = list(levels)

        if level is not None and not is_list_like(level):
            if not is_list_like(levels):
                raise TypeError("Levels must be list-like")
            if is_list_like(levels[0]):
                raise TypeError("Levels must be list-like")
            level = [level]
            levels = [levels]
        elif level is None or is_list_like(level):
            if not is_list_like(levels) or not is_list_like(levels[0]):
                raise TypeError("Levels must be list of lists-like")

        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._reset_identity()
        idx._set_levels(
            levels, level=level, validate=True, verify_integrity=verify_integrity
        )
        if not inplace:
            return idx
