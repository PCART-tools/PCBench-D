    def set_labels(self, labels, level=None, inplace=False, verify_integrity=True):
        """
        Set new labels on MultiIndex. Defaults to returning
        new index.

        Parameters
        ----------
        labels : sequence or list of sequence
            new labels to apply
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
        >>> idx.set_labels([[1,0,1,0], [0,0,1,1]])
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   labels=[[1, 0, 1, 0], [0, 0, 1, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_labels([1,0,1,0], level=0)
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   labels=[[1, 0, 1, 0], [0, 1, 0, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_labels([0,0,1,1], level='bar')
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   labels=[[0, 0, 1, 1], [0, 0, 1, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_labels([[1,0,1,0], [0,0,1,1]], level=[0,1])
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   labels=[[1, 0, 1, 0], [0, 0, 1, 1]],
                   names=[u'foo', u'bar'])
        """
        if level is not None and not is_list_like(level):
            if not is_list_like(labels):
                raise TypeError("Labels must be list-like")
            if is_list_like(labels[0]):
                raise TypeError("Labels must be list-like")
            level = [level]
            labels = [labels]
        elif level is None or is_list_like(level):
            if not is_list_like(labels) or not is_list_like(labels[0]):
                raise TypeError("Labels must be list of lists-like")

        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._reset_identity()
        idx._set_labels(labels, level=level, verify_integrity=verify_integrity)
        if not inplace:
            return idx
