    def to_pandas(  # noqa: D417
        self,
        *args: Any,
        use_pyarrow_extension_array: bool = False,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Cast to a pandas DataFrame.

        This requires that :mod:`pandas` and :mod:`pyarrow` are installed.
        This operation clones data, unless `use_pyarrow_extension_array=True`.

        Parameters
        ----------
        use_pyarrow_extension_array
            Use PyArrow backed-extension arrays instead of numpy arrays for each column
            of the pandas DataFrame; this allows zero copy operations and preservation
            of null values. Subsequent operations on the resulting pandas DataFrame may
            trigger conversion to NumPy arrays if that operation is not supported by
            pyarrow compute functions.
        **kwargs
            Arguments will be sent to :meth:`pyarrow.Table.to_pandas`.

        Returns
        -------
        :class:`pandas.DataFrame`

        Examples
        --------
        >>> import pandas
        >>> df1 = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> pandas_df1 = df1.to_pandas()
        >>> type(pandas_df1)
        <class 'pandas.core.frame.DataFrame'>
        >>> pandas_df1.dtypes
        foo     int64
        bar     int64
        ham    object
        dtype: object
        >>> df2 = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, None],
        ...         "bar": [6, None, 8],
        ...         "ham": [None, "b", "c"],
        ...     }
        ... )
        >>> pandas_df2 = df2.to_pandas()
        >>> pandas_df2
           foo  bar   ham
        0  1.0  6.0  None
        1  2.0  NaN     b
        2  NaN  8.0     c
        >>> pandas_df2.dtypes
        foo    float64
        bar    float64
        ham     object
        dtype: object
        >>> pandas_df2_pa = df2.to_pandas(
        ...     use_pyarrow_extension_array=True
        ... )  # doctest: +SKIP
        >>> pandas_df2_pa  # doctest: +SKIP
            foo   bar   ham
        0     1     6  <NA>
        1     2  <NA>     b
        2  <NA>     8     c
        >>> pandas_df2_pa.dtypes  # doctest: +SKIP
        foo           int64[pyarrow]
        bar           int64[pyarrow]
        ham    large_string[pyarrow]
        dtype: object

        """
        if use_pyarrow_extension_array:
            if parse_version(pd.__version__) < parse_version("1.5"):
                raise ModuleUpgradeRequired(
                    f'pandas>=1.5.0 is required for `to_pandas("use_pyarrow_extension_array=True")`, found Pandas {pd.__version__!r}'
                )
            if not _PYARROW_AVAILABLE or parse_version(pa.__version__) < (8, 0):
                msg = "pyarrow>=8.0.0 is required for `to_pandas(use_pyarrow_extension_array=True)`"
                if _PYARROW_AVAILABLE:
                    msg += f", found pyarrow {pa.__version__!r}."
                    raise ModuleUpgradeRequired(msg)
                else:
                    raise ModuleNotFoundError(msg)

        record_batches = self._df.to_pandas()
        tbl = pa.Table.from_batches(record_batches)
        if use_pyarrow_extension_array:
            return tbl.to_pandas(
                self_destruct=True,
                split_blocks=True,
                types_mapper=lambda pa_dtype: pd.ArrowDtype(pa_dtype),
                **kwargs,
            )

        date_as_object = kwargs.pop("date_as_object", False)
        return tbl.to_pandas(date_as_object=date_as_object, **kwargs)
