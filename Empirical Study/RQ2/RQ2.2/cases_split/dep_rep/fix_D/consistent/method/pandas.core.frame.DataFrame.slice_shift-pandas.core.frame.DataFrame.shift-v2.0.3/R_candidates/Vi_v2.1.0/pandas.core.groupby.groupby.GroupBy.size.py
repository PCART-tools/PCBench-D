    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def size(self) -> DataFrame | Series:
        """
        Compute group sizes.

        Returns
        -------
        DataFrame or Series
            Number of rows in each group as a Series if as_index is True
            or a DataFrame if as_index is False.
        %(see_also)s
        Examples
        --------

        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b']
        >>> ser = pd.Series([1, 2, 3], index=lst)
        >>> ser
        a     1
        a     2
        b     3
        dtype: int64
        >>> ser.groupby(level=0).size()
        a    2
        b    1
        dtype: int64

        >>> data = [[1, 2, 3], [1, 5, 6], [7, 8, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["owl", "toucan", "eagle"])
        >>> df
                a  b  c
        owl     1  2  3
        toucan  1  5  6
        eagle   7  8  9
        >>> df.groupby("a").size()
        a
        1    2
        7    1
        dtype: int64

        For Resampler:

        >>> ser = pd.Series([1, 2, 3], index=pd.DatetimeIndex(
        ...                 ['2023-01-01', '2023-01-15', '2023-02-01']))
        >>> ser
        2023-01-01    1
        2023-01-15    2
        2023-02-01    3
        dtype: int64
        >>> ser.resample('MS').size()
        2023-01-01    2
        2023-02-01    1
        Freq: MS, dtype: int64
        """
        result = self.grouper.size()
        dtype_backend: None | Literal["pyarrow", "numpy_nullable"] = None
        if isinstance(self.obj, Series):
            if isinstance(self.obj.array, ArrowExtensionArray):
                dtype_backend = "pyarrow"
            elif isinstance(self.obj.array, BaseMaskedArray):
                dtype_backend = "numpy_nullable"
        # TODO: For DataFrames what if columns are mixed arrow/numpy/masked?

        # GH28330 preserve subclassed Series/DataFrames through calls
        if isinstance(self.obj, Series):
            result = self._obj_1d_constructor(result, name=self.obj.name)
        else:
            result = self._obj_1d_constructor(result)

        if dtype_backend is not None:
            result = result.convert_dtypes(
                infer_objects=False,
                convert_string=False,
                convert_boolean=False,
                convert_floating=False,
                dtype_backend=dtype_backend,
            )

        with com.temp_setattr(self, "as_index", True):
            # size already has the desired behavior in GH#49519, but this makes the
            # as_index=False path of _reindex_output fail on categorical groupers.
            result = self._reindex_output(result, fill_value=0)
        if not self.as_index:
            # error: Incompatible types in assignment (expression has
            # type "DataFrame", variable has type "Series")
            result = result.rename("size").reset_index()  # type: ignore[assignment]
        return result
