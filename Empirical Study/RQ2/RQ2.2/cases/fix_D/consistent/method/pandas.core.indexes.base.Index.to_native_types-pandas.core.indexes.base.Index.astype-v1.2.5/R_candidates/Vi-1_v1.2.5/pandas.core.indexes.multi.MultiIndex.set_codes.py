    def set_codes(self, codes, level=None, inplace=None, verify_integrity=True):
        """
        Set new codes on MultiIndex. Defaults to returning new index.

        .. versionadded:: 0.24.0

           New name for deprecated method `set_labels`.

        Parameters
        ----------
        codes : sequence or list of sequence
            New codes to apply.
        level : int, level name, or sequence of int/level names (default None)
            Level(s) to set (None for all levels).
        inplace : bool
            If True, mutates in place.

            .. deprecated:: 1.2.0
        verify_integrity : bool (default True)
            If True, checks that levels and codes are compatible.

        Returns
        -------
        new index (of same type and class...etc) or None
            The same type as the caller or None if ``inplace=True``.

        Examples
        --------
        >>> idx = pd.MultiIndex.from_tuples(
        ...     [(1, "one"), (1, "two"), (2, "one"), (2, "two")], names=["foo", "bar"]
        ... )
        >>> idx
        MultiIndex([(1, 'one'),
            (1, 'two'),
            (2, 'one'),
            (2, 'two')],
           names=['foo', 'bar'])

        >>> idx.set_codes([[1, 0, 1, 0], [0, 0, 1, 1]])
        MultiIndex([(2, 'one'),
                    (1, 'one'),
                    (2, 'two'),
                    (1, 'two')],
                   names=['foo', 'bar'])
        >>> idx.set_codes([1, 0, 1, 0], level=0)
        MultiIndex([(2, 'one'),
                    (1, 'two'),
                    (2, 'one'),
                    (1, 'two')],
                   names=['foo', 'bar'])
        >>> idx.set_codes([0, 0, 1, 1], level='bar')
        MultiIndex([(1, 'one'),
                    (1, 'one'),
                    (2, 'two'),
                    (2, 'two')],
                   names=['foo', 'bar'])
        >>> idx.set_codes([[1, 0, 1, 0], [0, 0, 1, 1]], level=[0, 1])
        MultiIndex([(2, 'one'),
                    (1, 'one'),
                    (2, 'two'),
                    (1, 'two')],
                   names=['foo', 'bar'])
        """
        if inplace is not None:
            warnings.warn(
                "inplace is deprecated and will be removed in a future version.",
                FutureWarning,
                stacklevel=2,
            )
        else:
            inplace = False

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
