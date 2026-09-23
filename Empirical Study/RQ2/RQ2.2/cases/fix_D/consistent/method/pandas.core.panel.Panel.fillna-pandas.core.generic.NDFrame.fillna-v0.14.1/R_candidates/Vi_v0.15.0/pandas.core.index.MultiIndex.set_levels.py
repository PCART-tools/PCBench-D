    def set_levels(self, levels, level=None, inplace=False, verify_integrity=True):
        """
        Set new levels on MultiIndex. Defaults to returning
        new index.

        Parameters
        ----------
        levels : sequence or list of sequence
            new level(s) to apply
        level : int or level name, or sequence of int / level names (default None)
            level(s) to set (None for all levels)
        inplace : bool
            if True, mutates in place
        verify_integrity : bool (default True)
            if True, checks that levels and labels are compatible

        Returns
        -------
        new index (of same type and class...etc)


        Examples
        --------
        >>> idx = MultiIndex.from_tuples([(1, u'one'), (1, u'two'),
                                          (2, u'one'), (2, u'two')],
                                          names=['foo', 'bar'])
        >>> idx.set_levels([['a','b'], [1,2]])
        MultiIndex(levels=[[u'a', u'b'], [1, 2]],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_levels(['a','b'], level=0)
        MultiIndex(levels=[[u'a', u'b'], [u'one', u'two']],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_levels(['a','b'], level='bar')
        MultiIndex(levels=[[1, 2], [u'a', u'b']],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_levels([['a','b'], [1,2]], level=[0,1])
        MultiIndex(levels=[[u'a', u'b'], [1, 2]],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]],
                   names=[u'foo', u'bar'])
        """
        if level is not None and not com.is_list_like(level):
            if not com.is_list_like(levels):
                raise TypeError("Levels must be list-like")
            if com.is_list_like(levels[0]):
                raise TypeError("Levels must be list-like")
            level = [level]
            levels = [levels]
        elif level is None or com.is_list_like(level):
            if not com.is_list_like(levels) or not com.is_list_like(levels[0]):
                raise TypeError("Levels must be list of lists-like")

        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._reset_identity()
        idx._set_levels(levels, level=level, validate=True,
                        verify_integrity=verify_integrity)
        if not inplace:
            return idx
