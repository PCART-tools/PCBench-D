    @final
    def convert_dtypes(
        self: NDFrameT,
        infer_objects: bool_t = True,
        convert_string: bool_t = True,
        convert_integer: bool_t = True,
        convert_boolean: bool_t = True,
        convert_floating: bool_t = True,
        dtype_backend: DtypeBackend = "numpy_nullable",
    ) -> NDFrameT:
        """
        Convert columns to the best possible dtypes using dtypes supporting ``pd.NA``.

        Parameters
        ----------
        infer_objects : bool, default True
            Whether object dtypes should be converted to the best possible types.
        convert_string : bool, default True
            Whether object dtypes should be converted to ``StringDtype()``.
        convert_integer : bool, default True
            Whether, if possible, conversion can be done to integer extension types.
        convert_boolean : bool, defaults True
            Whether object dtypes should be converted to ``BooleanDtypes()``.
        convert_floating : bool, defaults True
            Whether, if possible, conversion can be done to floating extension types.
            If `convert_integer` is also True, preference will be give to integer
            dtypes if the floats can be faithfully casted to integers.

            .. versionadded:: 1.2.0
        dtype_backend : {"numpy_nullable", "pyarrow"}, default "numpy_nullable"
            Which dtype_backend to use, e.g. whether a DataFrame should use nullable
            dtypes for all dtypes that have a nullable
            implementation when "numpy_nullable" is set, pyarrow is used for all
            dtypes if "pyarrow" is set.

            The dtype_backends are still experimential.

            .. versionadded:: 2.0

        Returns
        -------
        Series or DataFrame
            Copy of input object with new dtype.

        See Also
        --------
        infer_objects : Infer dtypes of objects.
        to_datetime : Convert argument to datetime.
        to_timedelta : Convert argument to timedelta.
        to_numeric : Convert argument to a numeric type.

        Notes
        -----
        By default, ``convert_dtypes`` will attempt to convert a Series (or each
        Series in a DataFrame) to dtypes that support ``pd.NA``. By using the options
        ``convert_string``, ``convert_integer``, ``convert_boolean`` and
        ``convert_floating``, it is possible to turn off individual conversions
        to ``StringDtype``, the integer extension types, ``BooleanDtype``
        or floating extension types, respectively.

        For object-dtyped columns, if ``infer_objects`` is ``True``, use the inference
        rules as during normal Series/DataFrame construction.  Then, if possible,
        convert to ``StringDtype``, ``BooleanDtype`` or an appropriate integer
        or floating extension type, otherwise leave as ``object``.

        If the dtype is integer, convert to an appropriate integer extension type.

        If the dtype is numeric, and consists of all integers, convert to an
        appropriate integer extension type. Otherwise, convert to an
        appropriate floating extension type.

        .. versionchanged:: 1.2
            Starting with pandas 1.2, this method also converts float columns
            to the nullable floating extension type.

        In the future, as new dtypes are added that support ``pd.NA``, the results
        of this method will change to support those new dtypes.

        .. versionadded:: 2.0
            The nullable dtype implementation can be configured by calling
            ``pd.set_option("mode.dtype_backend", "pandas")`` to use
            numpy-backed nullable dtypes or
            ``pd.set_option("mode.dtype_backend", "pyarrow")`` to use
            pyarrow-backed nullable dtypes (using ``pd.ArrowDtype``).

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "a": pd.Series([1, 2, 3], dtype=np.dtype("int32")),
        ...         "b": pd.Series(["x", "y", "z"], dtype=np.dtype("O")),
        ...         "c": pd.Series([True, False, np.nan], dtype=np.dtype("O")),
        ...         "d": pd.Series(["h", "i", np.nan], dtype=np.dtype("O")),
        ...         "e": pd.Series([10, np.nan, 20], dtype=np.dtype("float")),
        ...         "f": pd.Series([np.nan, 100.5, 200], dtype=np.dtype("float")),
        ...     }
        ... )

        Start with a DataFrame with default dtypes.

        >>> df
           a  b      c    d     e      f
        0  1  x   True    h  10.0    NaN
        1  2  y  False    i   NaN  100.5
        2  3  z    NaN  NaN  20.0  200.0

        >>> df.dtypes
        a      int32
        b     object
        c     object
        d     object
        e    float64
        f    float64
        dtype: object

        Convert the DataFrame to use best possible dtypes.

        >>> dfn = df.convert_dtypes()
        >>> dfn
           a  b      c     d     e      f
        0  1  x   True     h    10   <NA>
        1  2  y  False     i  <NA>  100.5
        2  3  z   <NA>  <NA>    20  200.0

        >>> dfn.dtypes
        a             Int32
        b    string[python]
        c           boolean
        d    string[python]
        e             Int64
        f           Float64
        dtype: object

        Start with a Series of strings and missing data represented by ``np.nan``.

        >>> s = pd.Series(["a", "b", np.nan])
        >>> s
        0      a
        1      b
        2    NaN
        dtype: object

        Obtain a Series with dtype ``StringDtype``.

        >>> s.convert_dtypes()
        0       a
        1       b
        2    <NA>
        dtype: string
        """
        check_dtype_backend(dtype_backend)
        if self.ndim == 1:
            return self._convert_dtypes(
                infer_objects,
                convert_string,
                convert_integer,
                convert_boolean,
                convert_floating,
                dtype_backend=dtype_backend,
            )
        else:
            results = [
                col._convert_dtypes(
                    infer_objects,
                    convert_string,
                    convert_integer,
                    convert_boolean,
                    convert_floating,
                    dtype_backend=dtype_backend,
                )
                for col_name, col in self.items()
            ]
            if len(results) > 0:
                result = concat(results, axis=1, copy=False, keys=self.columns)
                cons = cast(Type["DataFrame"], self._constructor)
                result = cons(result)
                result = result.__finalize__(self, method="convert_dtypes")
                # https://github.com/python/mypy/issues/8354
                return cast(NDFrameT, result)
            else:
                return self.copy(deep=None)
