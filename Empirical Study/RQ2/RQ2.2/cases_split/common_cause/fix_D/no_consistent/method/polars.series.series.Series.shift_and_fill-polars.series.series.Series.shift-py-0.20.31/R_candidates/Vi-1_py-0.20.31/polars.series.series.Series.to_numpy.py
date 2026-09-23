    def to_numpy(
        self,
        *,
        writable: bool = False,
        allow_copy: bool = True,
        use_pyarrow: bool | None = None,
        zero_copy_only: bool | None = None,
    ) -> np.ndarray[Any, Any]:
        """
        Convert this Series to a NumPy ndarray.

        This operation copies data only when necessary. The conversion is zero copy when
        all of the following hold:

        - The data type is an integer, float, `Datetime`, `Duration`, or `Array`.
        - The Series contains no null values.
        - The Series consists of a single chunk.
        - The `writable` parameter is set to `False` (default).

        Parameters
        ----------
        writable
            Ensure the resulting array is writable. This will force a copy of the data
            if the array was created without copy as the underlying Arrow data is
            immutable.
        allow_copy
            Allow memory to be copied to perform the conversion. If set to `False`,
            causes conversions that are not zero-copy to fail.

        use_pyarrow
            First convert to PyArrow, then call `pyarrow.Array.to_numpy
            <https://arrow.apache.org/docs/python/generated/pyarrow.Array.html#pyarrow.Array.to_numpy>`_
            to convert to NumPy. If set to `False`, Polars' own conversion logic is
            used.

            .. deprecated:: 0.20.28
                Polars now uses its native engine by default for conversion to NumPy.
                To use PyArrow's engine, call `.to_arrow().to_numpy()` instead.

        zero_copy_only
            Raise an exception if the conversion to a NumPy would require copying
            the underlying data. Data copy occurs, for example, when the Series contains
            nulls or non-numeric types.

            .. deprecated:: 0.20.10
                Use the `allow_copy` parameter instead, which is the inverse of this
                one.

        Examples
        --------
        Numeric data without nulls can be converted without copying data.
        The resulting array will not be writable.

        >>> s = pl.Series([1, 2, 3], dtype=pl.Int8)
        >>> arr = s.to_numpy()
        >>> arr
        array([1, 2, 3], dtype=int8)
        >>> arr.flags.writeable
        False

        Set `writable=True` to force data copy to make the array writable.

        >>> s.to_numpy(writable=True).flags.writeable
        True

        Integer Series containing nulls will be cast to a float type with `nan`
        representing a null value. This requires data to be copied.

        >>> s = pl.Series([1, 2, None], dtype=pl.UInt16)
        >>> s.to_numpy()
        array([ 1.,  2., nan], dtype=float32)

        Set `allow_copy=False` to raise an error if data would be copied.

        >>> s.to_numpy(allow_copy=False)  # doctest: +SKIP
        Traceback (most recent call last):
        ...
        RuntimeError: copy not allowed: cannot convert to a NumPy array without copying data

        Series of data type `Array` and `Struct` will result in an array with more than
        one dimension.

        >>> s = pl.Series([[1, 2, 3], [4, 5, 6]], dtype=pl.Array(pl.Int64, 3))
        >>> s.to_numpy()
        array([[1, 2, 3],
               [4, 5, 6]])
        """  # noqa: W505
        if zero_copy_only is not None:
            issue_deprecation_warning(
                "The `zero_copy_only` parameter for `Series.to_numpy` is deprecated."
                " Use the `allow_copy` parameter instead, which is the inverse of `zero_copy_only`.",
                version="0.20.10",
            )
            allow_copy = not zero_copy_only

        if use_pyarrow is not None:
            issue_deprecation_warning(
                "The `use_pyarrow` parameter for `Series.to_numpy` is deprecated."
                " Polars now uses its native engine for conversion to NumPy by default."
                " To use PyArrow's engine, call `.to_arrow().to_numpy()` instead.",
                version="0.20.28",
            )
        else:
            use_pyarrow = False

        if (
            use_pyarrow
            and _PYARROW_AVAILABLE
            and self.dtype not in (Date, Datetime, Duration, Array, Object)
        ):
            if not allow_copy and self.n_chunks() > 1 and not self.is_empty():
                msg = "cannot return a zero-copy array"
                raise ValueError(msg)

            return self.to_arrow().to_numpy(
                zero_copy_only=not allow_copy, writable=writable
            )

        return self._s.to_numpy(writable=writable, allow_copy=allow_copy)
