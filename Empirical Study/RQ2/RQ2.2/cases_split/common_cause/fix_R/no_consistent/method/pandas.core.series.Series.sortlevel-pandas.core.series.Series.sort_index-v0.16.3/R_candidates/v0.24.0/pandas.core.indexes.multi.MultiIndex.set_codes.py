    @deprecate_kwarg(old_arg_name='labels', new_arg_name='codes')
    def set_codes(self, codes, level=None, inplace=False,
                  verify_integrity=True):
        """
        Set new codes on MultiIndex. Defaults to returning
        new index.

        .. versionadded:: 0.24.0

           New name for deprecated method `set_labels`.

        Parameters
        ----------
        codes : sequence or list of sequence
            new codes to apply
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
        >>> idx = pd.MultiIndex.from_tuples([(1, u'one'), (1, u'two'),
                                            (2, u'one'), (2, u'two')],
                                            names=['foo', 'bar'])
        >>> idx.set_codes([[1,0,1,0], [0,0,1,1]])
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   codes=[[1, 0, 1, 0], [0, 0, 1, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_codes([1,0,1,0], level=0)
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   codes=[[1, 0, 1, 0], [0, 1, 0, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_codes([0,0,1,1], level='bar')
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   codes=[[0, 0, 1, 1], [0, 0, 1, 1]],
                   names=[u'foo', u'bar'])
        >>> idx.set_codes([[1,0,1,0], [0,0,1,1]], level=[0,1])
        MultiIndex(levels=[[1, 2], [u'one', u'two']],
                   codes=[[1, 0, 1, 0], [0, 0, 1, 1]],
                   names=[u'foo', u'bar'])
        """
        if level is not None and not is_list_like(level):
            if not is_list_like(codes):
                raise TypeError("Codes must be list-like")
            if is_list_like(codes[0]):
                raise TypeError("Codes must be list-like")
            level = [level]
            codes = [codes]
        elif level is None or is_list_like(level):
            if not is_list_like(codes) or not is_list_like(codes[0]):
                raise TypeError("Codes must be list of lists-like")

        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._reset_identity()
        idx._set_codes(codes, level=level, verify_integrity=verify_integrity)
        if not inplace:
            return idx
