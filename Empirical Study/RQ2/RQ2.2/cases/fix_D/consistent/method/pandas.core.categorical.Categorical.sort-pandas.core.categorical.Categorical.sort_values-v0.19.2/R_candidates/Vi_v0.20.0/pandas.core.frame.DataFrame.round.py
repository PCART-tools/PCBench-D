    def round(self, decimals=0, *args, **kwargs):
        """
        Round a DataFrame to a variable number of decimal places.

        .. versionadded:: 0.17.0

        Parameters
        ----------
        decimals : int, dict, Series
            Number of decimal places to round each column to. If an int is
            given, round each column to the same number of places.
            Otherwise dict and Series round to variable numbers of places.
            Column names should be in the keys if `decimals` is a
            dict-like, or in the index if `decimals` is a Series. Any
            columns not included in `decimals` will be left as is. Elements
            of `decimals` which are not columns of the input will be
            ignored.

        Examples
        --------
        >>> df = pd.DataFrame(np.random.random([3, 3]),
        ...     columns=['A', 'B', 'C'], index=['first', 'second', 'third'])
        >>> df
                       A         B         C
        first   0.028208  0.992815  0.173891
        second  0.038683  0.645646  0.577595
        third   0.877076  0.149370  0.491027
        >>> df.round(2)
                   A     B     C
        first   0.03  0.99  0.17
        second  0.04  0.65  0.58
        third   0.88  0.15  0.49
        >>> df.round({'A': 1, 'C': 2})
                  A         B     C
        first   0.0  0.992815  0.17
        second  0.0  0.645646  0.58
        third   0.9  0.149370  0.49
        >>> decimals = pd.Series([1, 0, 2], index=['A', 'B', 'C'])
        >>> df.round(decimals)
                  A  B     C
        first   0.0  1  0.17
        second  0.0  1  0.58
        third   0.9  0  0.49

        Returns
        -------
        DataFrame object

        See Also
        --------
        numpy.around
        Series.round

        """
        from pandas.core.reshape.concat import concat

        def _dict_round(df, decimals):
            for col, vals in df.iteritems():
                try:
                    yield _series_round(vals, decimals[col])
                except KeyError:
                    yield vals

        def _series_round(s, decimals):
            if is_integer_dtype(s) or is_float_dtype(s):
                return s.round(decimals)
            return s

        nv.validate_round(args, kwargs)

        if isinstance(decimals, (dict, Series)):
            if isinstance(decimals, Series):
                if not decimals.index.is_unique:
                    raise ValueError("Index of decimals must be unique")
            new_cols = [col for col in _dict_round(self, decimals)]
        elif is_integer(decimals):
            # Dispatch to Series.round
            new_cols = [_series_round(v, decimals)
                        for _, v in self.iteritems()]
        else:
            raise TypeError("decimals must be an integer, a dict-like or a "
                            "Series")

        if len(new_cols) > 0:
            return self._constructor(concat(new_cols, axis=1),
                                     index=self.index,
                                     columns=self.columns)
        else:
            return self
