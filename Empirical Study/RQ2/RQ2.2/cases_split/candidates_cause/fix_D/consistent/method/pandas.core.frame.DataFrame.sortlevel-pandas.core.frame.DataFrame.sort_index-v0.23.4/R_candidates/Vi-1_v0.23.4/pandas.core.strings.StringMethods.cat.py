    def cat(self, others=None, sep=None, na_rep=None, join=None):
        """
        Concatenate strings in the Series/Index with given separator.

        If `others` is specified, this function concatenates the Series/Index
        and elements of `others` element-wise.
        If `others` is not passed, then all values in the Series/Index are
        concatenated into a single string with a given `sep`.

        Parameters
        ----------
        others : Series, Index, DataFrame, np.ndarrary or list-like
            Series, Index, DataFrame, np.ndarray (one- or two-dimensional) and
            other list-likes of strings must have the same length as the
            calling Series/Index, with the exception of indexed objects (i.e.
            Series/Index/DataFrame) if `join` is not None.

            If others is a list-like that contains a combination of Series,
            np.ndarray (1-dim) or list-like, then all elements will be unpacked
            and must satisfy the above criteria individually.

            If others is None, the method returns the concatenation of all
            strings in the calling Series/Index.
        sep : string or None, default None
            If None, concatenates without any separator.
        na_rep : string or None, default None
            Representation that is inserted for all missing values:

            - If `na_rep` is None, and `others` is None, missing values in the
              Series/Index are omitted from the result.
            - If `na_rep` is None, and `others` is not None, a row containing a
              missing value in any of the columns (before concatenation) will
              have a missing value in the result.
        join : {'left', 'right', 'outer', 'inner'}, default None
            Determines the join-style between the calling Series/Index and any
            Series/Index/DataFrame in `others` (objects without an index need
            to match the length of the calling Series/Index). If None,
            alignment is disabled, but this option will be removed in a future
            version of pandas and replaced with a default of `'left'`. To
            disable alignment, use `.values` on any Series/Index/DataFrame in
            `others`.

            .. versionadded:: 0.23.0

        Returns
        -------
        concat : str or Series/Index of objects
            If `others` is None, `str` is returned, otherwise a `Series/Index`
            (same type as caller) of objects is returned.

        See Also
        --------
        split : Split each string in the Series/Index

        Examples
        --------
        When not passing `others`, all values are concatenated into a single
        string:

        >>> s = pd.Series(['a', 'b', np.nan, 'd'])
        >>> s.str.cat(sep=' ')
        'a b d'

        By default, NA values in the Series are ignored. Using `na_rep`, they
        can be given a representation:

        >>> s.str.cat(sep=' ', na_rep='?')
        'a b ? d'

        If `others` is specified, corresponding values are concatenated with
        the separator. Result will be a Series of strings.

        >>> s.str.cat(['A', 'B', 'C', 'D'], sep=',')
        0    a,A
        1    b,B
        2    NaN
        3    d,D
        dtype: object

        Missing values will remain missing in the result, but can again be
        represented using `na_rep`

        >>> s.str.cat(['A', 'B', 'C', 'D'], sep=',', na_rep='-')
        0    a,A
        1    b,B
        2    -,C
        3    d,D
        dtype: object

        If `sep` is not specified, the values are concatenated without
        separation.

        >>> s.str.cat(['A', 'B', 'C', 'D'], na_rep='-')
        0    aA
        1    bB
        2    -C
        3    dD
        dtype: object

        Series with different indexes can be aligned before concatenation. The
        `join`-keyword works as in other methods.

        >>> t = pd.Series(['d', 'a', 'e', 'c'], index=[3, 0, 4, 2])
        >>> s.str.cat(t, join=None, na_rep='-')
        0    ad
        1    ba
        2    -e
        3    dc
        dtype: object
        >>>
        >>> s.str.cat(t, join='left', na_rep='-')
        0    aa
        1    b-
        2    -c
        3    dd
        dtype: object
        >>>
        >>> s.str.cat(t, join='outer', na_rep='-')
        0    aa
        1    b-
        2    -c
        3    dd
        4    -e
        dtype: object
        >>>
        >>> s.str.cat(t, join='inner', na_rep='-')
        0    aa
        2    -c
        3    dd
        dtype: object
        >>>
        >>> s.str.cat(t, join='right', na_rep='-')
        3    dd
        0    aa
        4    -e
        2    -c
        dtype: object

        For more examples, see :ref:`here <text.concatenate>`.
        """
        from pandas import Index, Series, concat

        if isinstance(others, compat.string_types):
            raise ValueError("Did you mean to supply a `sep` keyword?")

        if isinstance(self._orig, Index):
            data = Series(self._orig, index=self._orig)
        else:  # Series
            data = self._orig

        # concatenate Series/Index with itself if no "others"
        if others is None:
            result = str_cat(data, others=others, sep=sep, na_rep=na_rep)
            return self._wrap_result(result,
                                     use_codes=(not self._is_categorical))

        try:
            # turn anything in "others" into lists of Series
            others, warn = self._get_series_list(others,
                                                 ignore_index=(join is None))
        except ValueError:  # do not catch TypeError raised by _get_series_list
            if join is None:
                raise ValueError('All arrays must be same length, except '
                                 'those having an index if `join` is not None')
            else:
                raise ValueError('If `others` contains arrays or lists (or '
                                 'other list-likes without an index), these '
                                 'must all be of the same length as the '
                                 'calling Series/Index.')

        if join is None and warn:
            warnings.warn("A future version of pandas will perform index "
                          "alignment when `others` is a Series/Index/"
                          "DataFrame (or a list-like containing one). To "
                          "disable alignment (the behavior before v.0.23) and "
                          "silence this warning, use `.values` on any Series/"
                          "Index/DataFrame in `others`. To enable alignment "
                          "and silence this warning, pass `join='left'|"
                          "'outer'|'inner'|'right'`. The future default will "
                          "be `join='left'`.", FutureWarning, stacklevel=2)

        # align if required
        if join is not None:
            # Need to add keys for uniqueness in case of duplicate columns
            others = concat(others, axis=1,
                            join=(join if join == 'inner' else 'outer'),
                            keys=range(len(others)))
            data, others = data.align(others, join=join)
            others = [others[x] for x in others]  # again list of Series

        # str_cat discards index
        res = str_cat(data, others=others, sep=sep, na_rep=na_rep)

        if isinstance(self._orig, Index):
            res = Index(res, name=self._orig.name)
        else:  # Series
            res = Series(res, index=data.index, name=self._orig.name)
        return res
