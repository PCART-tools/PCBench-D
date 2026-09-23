    def to_pandas(
        self,
        *,
        use_pyarrow_extension_array: bool = False,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Convert this DataFrame to a pandas DataFrame.

        This operation copies data if `use_pyarrow_extension_array` is not enabled.

        Parameters
        ----------
        use_pyarrow_extension_array
            Use PyArrow-backed extension arrays instead of NumPy arrays for the columns
            of the pandas DataFrame. This allows zero copy operations and preservation
            of null values. Subsequent operations on the resulting pandas DataFrame may
            trigger conversion to NumPy if those operations are not supported by PyArrow
            compute functions.
        **kwargs
            Additional keyword arguments to be passed to
            :meth:`pyarrow.Table.to_pandas`.

        Returns
        -------
        :class:`pandas.DataFrame`

        Notes
        -----
        This operation requires that both :mod:`pandas` and :mod:`pyarrow` are
        installed.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.to_pandas()
           foo  bar ham
        0    1  6.0   a
        1    2  7.0   b
        2    3  8.0   c

        Null values in numeric columns are converted to `NaN`.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, None],
        ...         "bar": [6.0, None, 8.0],
        ...         "ham": [None, "b", "c"],
        ...     }
        ... )
        >>> df.to_pandas()
           foo  bar   ham
        0  1.0  6.0  None
        1  2.0  NaN     b
        2  NaN  8.0     c

        Pass `use_pyarrow_extension_array=True` to get a pandas DataFrame with columns
        backed by PyArrow extension arrays. This will preserve null values.

        >>> df.to_pandas(use_pyarrow_extension_array=True)
            foo   bar   ham
        0     1   6.0  <NA>
        1     2  <NA>     b
        2  <NA>   8.0     c
        >>> _.dtypes
        foo           int64[pyarrow]
        bar          double[pyarrow]
        ham    large_string[pyarrow]
        dtype: object
        """
        if use_pyarrow_extension_array:
            if parse_version(pd.__version__) < (1, 5):
                msg = f'pandas>=1.5.0 is required for `to_pandas("use_pyarrow_extension_array=True")`, found Pandas {pd.__version__!r}'
                raise ModuleUpgradeRequiredError(msg)
            if not _PYARROW_AVAILABLE or parse_version(pa.__version__) < (8, 0):
                msg = "pyarrow>=8.0.0 is required for `to_pandas(use_pyarrow_extension_array=True)`"
                if _PYARROW_AVAILABLE:
                    msg += f", found pyarrow {pa.__version__!r}."
                    raise ModuleUpgradeRequiredError(msg)
                else:
                    raise ModuleNotFoundError(msg)

        # Object columns must be handled separately as Arrow does not convert them
        # correctly
        if Object in self.dtypes:
            return self._to_pandas_with_object_columns(
                use_pyarrow_extension_array=use_pyarrow_extension_array, **kwargs
            )

        return self._to_pandas_without_object_columns(
            self, use_pyarrow_extension_array=use_pyarrow_extension_array, **kwargs
        )
