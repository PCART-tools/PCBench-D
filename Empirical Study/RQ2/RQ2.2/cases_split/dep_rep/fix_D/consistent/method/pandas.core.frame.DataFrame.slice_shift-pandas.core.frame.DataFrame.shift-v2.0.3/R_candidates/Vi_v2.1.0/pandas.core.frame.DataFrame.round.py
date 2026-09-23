    def round(
        self, decimals: int | dict[IndexLabel, int] | Series = 0, *args, **kwargs
    ) -> DataFrame:
        """
        Round a DataFrame to a variable number of decimal places.

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
        *args
            Additional keywords have no effect but might be accepted for
            compatibility with numpy.
        **kwargs
            Additional keywords have no effect but might be accepted for
            compatibility with numpy.

        Returns
        -------
        DataFrame
            A DataFrame with the affected columns rounded to the specified
            number of decimal places.

        See Also
        --------
        numpy.around : Round a numpy array to the given number of decimals.
        Series.round : Round a Series to the given number of decimals.

        Examples
        --------
        >>> df = pd.DataFrame([(.21, .32), (.01, .67), (.66, .03), (.21, .18)],
        ...                   columns=['dogs', 'cats'])
        >>> df
            dogs  cats
        0  0.21  0.32
        1  0.01  0.67
        2  0.66  0.03
        3  0.21  0.18

        By providing an integer each column is rounded to the same number
        of decimal places

        >>> df.round(1)
            dogs  cats
        0   0.2   0.3
        1   0.0   0.7
        2   0.7   0.0
        3   0.2   0.2

        With a dict, the number of places for specific columns can be
        specified with the column names as key and the number of decimal
        places as value

        >>> df.round({'dogs': 1, 'cats': 0})
            dogs  cats
        0   0.2   0.0
        1   0.0   1.0
        2   0.7   0.0
        3   0.2   0.0

        Using a Series, the number of places for specific columns can be
        specified with the column names as index and the number of
        decimal places as value

        >>> decimals = pd.Series([0, 1], index=['cats', 'dogs'])
        >>> df.round(decimals)
            dogs  cats
        0   0.2   0.0
        1   0.0   1.0
        2   0.7   0.0
        3   0.2   0.0
        """
        from pandas.core.reshape.concat import concat

        def _dict_round(df: DataFrame, decimals):
            for col, vals in df.items():
                try:
                    yield _series_round(vals, decimals[col])
                except KeyError:
                    yield vals

        def _series_round(ser: Series, decimals: int) -> Series:
            if is_integer_dtype(ser.dtype) or is_float_dtype(ser.dtype):
                return ser.round(decimals)
            return ser

        nv.validate_round(args, kwargs)

        if isinstance(decimals, (dict, Series)):
            if isinstance(decimals, Series) and not decimals.index.is_unique:
                raise ValueError("Index of decimals must be unique")
            if is_dict_like(decimals) and not all(
                is_integer(value) for _, value in decimals.items()
            ):
                raise TypeError("Values in decimals must be integers")
            new_cols = list(_dict_round(self, decimals))
        elif is_integer(decimals):
            # Dispatch to Block.round
            # Argument "decimals" to "round" of "BaseBlockManager" has incompatible
            # type "Union[int, integer[Any]]"; expected "int"
            new_mgr = self._mgr.round(
                decimals=decimals,  # type: ignore[arg-type]
                using_cow=using_copy_on_write(),
            )
            return self._constructor_from_mgr(new_mgr, axes=new_mgr.axes).__finalize__(
                self, method="round"
            )
        else:
            raise TypeError("decimals must be an integer, a dict-like or a Series")

        if new_cols is not None and len(new_cols) > 0:
            return self._constructor(
                concat(new_cols, axis=1), index=self.index, columns=self.columns
            ).__finalize__(self, method="round")
        else:
            return self.copy(deep=False)
