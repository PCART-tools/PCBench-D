    def set_names(self, names, level=None, inplace=False):
        """
        Set new names on index. Defaults to returning new index.

        Parameters
        ----------
        names : str or sequence
            name(s) to set
        level : int, level name, or sequence of int/level names (default None)
            If the index is a MultiIndex (hierarchical), level(s) to set (None
            for all levels).  Otherwise level must be None
        inplace : bool
            if True, mutates in place

        Returns
        -------
        new index (of same type and class...etc) [if inplace, returns None]

        Examples
        --------
        >>> Index([1, 2, 3, 4]).set_names('foo')
        Int64Index([1, 2, 3, 4], dtype='int64', name='foo')
        >>> Index([1, 2, 3, 4]).set_names(['foo'])
        Int64Index([1, 2, 3, 4], dtype='int64', name='foo')
        >>> idx = MultiIndex.from_tuples([(1, u'one'), (1, u'two'),
                                          (2, u'one'), (2, u'two')],
                                          names=['foo', 'bar'])
        >>> idx.set_names(['baz', 'quz'])
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]],
                   names=[u'baz', u'quz'])
        >>> idx.set_names('baz', level=0)
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]],
                   names=[u'baz', u'bar'])
        """

        from .multi import MultiIndex
        if level is not None and not isinstance(self, MultiIndex):
            raise ValueError('Level must be None for non-MultiIndex')

        if level is not None and not is_list_like(level) and is_list_like(
                names):
            raise TypeError("Names must be a string")

        if not is_list_like(names) and level is None and self.nlevels > 1:
            raise TypeError("Must pass list-like as `names`.")

        if not is_list_like(names):
            names = [names]
        if level is not None and not is_list_like(level):
            level = [level]

        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._set_names(names, level=level)
        if not inplace:
            return idx
