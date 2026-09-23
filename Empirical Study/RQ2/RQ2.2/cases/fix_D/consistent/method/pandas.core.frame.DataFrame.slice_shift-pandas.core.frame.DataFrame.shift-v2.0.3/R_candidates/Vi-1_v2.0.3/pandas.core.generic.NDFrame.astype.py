    def astype(
        self: NDFrameT, dtype, copy: bool_t | None = None, errors: IgnoreRaise = "raise"
    ) -> NDFrameT:
        """
        Cast a pandas object to a specified dtype ``dtype``.

        Parameters
        ----------
        dtype : str, data type, Series or Mapping of column name -> data type
            Use a str, numpy.dtype, pandas.ExtensionDtype or Python type to
            cast entire pandas object to the same type. Alternatively, use a
            mapping, e.g. {col: dtype, ...}, where col is a column label and dtype is
            a numpy.dtype or Python type to cast one or more of the DataFrame's
            columns to column-specific types.
        copy : bool, default True
            Return a copy when ``copy=True`` (be very careful setting
            ``copy=False`` as changes to values then may propagate to other
            pandas objects).
        errors : {'raise', 'ignore'}, default 'raise'
            Control raising of exceptions on invalid data for provided dtype.

            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object.

        Returns
        -------
        same type as caller

        See Also
        --------
        to_datetime : Convert argument to datetime.
        to_timedelta : Convert argument to timedelta.
        to_numeric : Convert argument to a numeric type.
        numpy.ndarray.astype : Cast a numpy array to a specified type.

        Notes
        -----
        .. versionchanged:: 2.0.0

            Using ``astype`` to convert from timezone-naive dtype to
            timezone-aware dtype will raise an exception.
            Use :meth:`Series.dt.tz_localize` instead.

        Examples
        --------
        Create a DataFrame:

        >>> d = {'col1': [1, 2], 'col2': [3, 4]}
        >>> df = pd.DataFrame(data=d)
        >>> df.dtypes
        col1    int64
        col2    int64
        dtype: object

        Cast all columns to int32:

        >>> df.astype('int32').dtypes
        col1    int32
        col2    int32
        dtype: object

        Cast col1 to int32 using a dictionary:

        >>> df.astype({'col1': 'int32'}).dtypes
        col1    int32
        col2    int64
        dtype: object

        Create a series:

        >>> ser = pd.Series([1, 2], dtype='int32')
        >>> ser
        0    1
        1    2
        dtype: int32
        >>> ser.astype('int64')
        0    1
        1    2
        dtype: int64

        Convert to categorical type:

        >>> ser.astype('category')
        0    1
        1    2
        dtype: category
        Categories (2, int32): [1, 2]

        Convert to ordered categorical type with custom ordering:

        >>> from pandas.api.types import CategoricalDtype
        >>> cat_dtype = CategoricalDtype(
        ...     categories=[2, 1], ordered=True)
        >>> ser.astype(cat_dtype)
        0    1
        1    2
        dtype: category
        Categories (2, int64): [2 < 1]

        Create a series of dates:

        >>> ser_date = pd.Series(pd.date_range('20200101', periods=3))
        >>> ser_date
        0   2020-01-01
        1   2020-01-02
        2   2020-01-03
        dtype: datetime64[ns]
        """
        if copy and using_copy_on_write():
            copy = False

        if is_dict_like(dtype):
            if self.ndim == 1:  # i.e. Series
                if len(dtype) > 1 or self.name not in dtype:
                    raise KeyError(
                        "Only the Series name can be used for "
                        "the key in Series dtype mappings."
                    )
                new_type = dtype[self.name]
                return self.astype(new_type, copy, errors)

            # GH#44417 cast to Series so we can use .iat below, which will be
            #  robust in case we
            from pandas import Series

            dtype_ser = Series(dtype, dtype=object)

            for col_name in dtype_ser.index:
                if col_name not in self:
                    raise KeyError(
                        "Only a column name can be used for the "
                        "key in a dtype mappings argument. "
                        f"'{col_name}' not found in columns."
                    )

            dtype_ser = dtype_ser.reindex(self.columns, fill_value=None, copy=False)

            results = []
            for i, (col_name, col) in enumerate(self.items()):
                cdt = dtype_ser.iat[i]
                if isna(cdt):
                    res_col = col.copy(deep=copy)
                else:
                    try:
                        res_col = col.astype(dtype=cdt, copy=copy, errors=errors)
                    except ValueError as ex:
                        ex.args = (
                            f"{ex}: Error while type casting for column '{col_name}'",
                        )
                        raise
                results.append(res_col)

        elif is_extension_array_dtype(dtype) and self.ndim > 1:
            # GH 18099/22869: columnwise conversion to extension dtype
            # GH 24704: use iloc to handle duplicate column names
            # TODO(EA2D): special case not needed with 2D EAs
            results = [
                self.iloc[:, i].astype(dtype, copy=copy)
                for i in range(len(self.columns))
            ]

        else:
            # else, only a single dtype is given
            new_data = self._mgr.astype(dtype=dtype, copy=copy, errors=errors)
            return self._constructor(new_data).__finalize__(self, method="astype")

        # GH 33113: handle empty frame or series
        if not results:
            return self.copy(deep=None)

        # GH 19920: retain column metadata after concat
        result = concat(results, axis=1, copy=False)
        # GH#40810 retain subclass
        # error: Incompatible types in assignment
        # (expression has type "NDFrameT", variable has type "DataFrame")
        result = self._constructor(result)  # type: ignore[assignment]
        result.columns = self.columns
        result = result.__finalize__(self, method="astype")
        # https://github.com/python/mypy/issues/8354
        return cast(NDFrameT, result)
