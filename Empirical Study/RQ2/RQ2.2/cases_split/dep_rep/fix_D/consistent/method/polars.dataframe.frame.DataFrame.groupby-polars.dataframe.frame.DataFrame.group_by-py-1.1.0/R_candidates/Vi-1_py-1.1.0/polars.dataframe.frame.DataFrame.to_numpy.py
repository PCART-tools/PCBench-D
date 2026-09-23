    def to_numpy(
        self,
        *,
        order: IndexOrder = "fortran",
        writable: bool = False,
        allow_copy: bool = True,
        structured: bool = False,
        use_pyarrow: bool | None = None,
    ) -> np.ndarray[Any, Any]:
        """
        Convert this DataFrame to a NumPy ndarray.

        This operation copies data only when necessary. The conversion is zero copy when
        all of the following hold:

        - The DataFrame is fully contiguous in memory, with all Series back-to-back and
          all Series consisting of a single chunk.
        - The data type is an integer or float.
        - The DataFrame contains no null values.
        - The `order` parameter is set to `fortran` (default).
        - The `writable` parameter is set to `False` (default).

        Parameters
        ----------
        order
            The index order of the returned NumPy array, either C-like or
            Fortran-like. In general, using the Fortran-like index order is faster.
            However, the C-like order might be more appropriate to use for downstream
            applications to prevent cloning data, e.g. when reshaping into a
            one-dimensional array.
        writable
            Ensure the resulting array is writable. This will force a copy of the data
            if the array was created without copy, as the underlying Arrow data is
            immutable.
        allow_copy
            Allow memory to be copied to perform the conversion. If set to `False`,
            causes conversions that are not zero-copy to fail.
        structured
            Return a `structured array`_ with a data type that corresponds to the
            DataFrame schema. If set to `False` (default), a 2D ndarray is
            returned instead.

            .. _structured array: https://numpy.org/doc/stable/user/basics.rec.html

        use_pyarrow
            Use `pyarrow.Array.to_numpy
            <https://arrow.apache.org/docs/python/generated/pyarrow.Array.html#pyarrow.Array.to_numpy>`_

            function for the conversion to NumPy if necessary.

            .. deprecated:: 0.20.28
                Polars now uses its native engine by default for conversion to NumPy.

        Examples
        --------
        Numeric data without nulls can be converted without copying data in some cases.
        The resulting array will not be writable.

        >>> df = pl.DataFrame({"a": [1, 2, 3]})
        >>> arr = df.to_numpy()
        >>> arr
        array([[1],
               [2],
               [3]])
        >>> arr.flags.writeable
        False

        Set `writable=True` to force data copy to make the array writable.

        >>> df.to_numpy(writable=True).flags.writeable
        True

        If the DataFrame contains different numeric data types, the resulting data type
        will be the supertype. This requires data to be copied. Integer types with
        nulls are cast to a float type with `nan` representing a null value.

        >>> df = pl.DataFrame({"a": [1, 2, None], "b": [4.0, 5.0, 6.0]})
        >>> df.to_numpy()
        array([[ 1.,  4.],
               [ 2.,  5.],
               [nan,  6.]])

        Set `allow_copy=False` to raise an error if data would be copied.

        >>> s.to_numpy(allow_copy=False)  # doctest: +SKIP
        Traceback (most recent call last):
        ...
        RuntimeError: copy not allowed: cannot convert to a NumPy array without copying data

        Polars defaults to F-contiguous order. Use `order="c"` to force the resulting
        array to be C-contiguous.

        >>> df.to_numpy(order="c").flags.c_contiguous
        True

        DataFrames with mixed types will result in an array with an object dtype.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.5, 7.0, 8.5],
        ...         "ham": ["a", "b", "c"],
        ...     },
        ...     schema_overrides={"foo": pl.UInt8, "bar": pl.Float32},
        ... )
        >>> df.to_numpy()
        array([[1, 6.5, 'a'],
               [2, 7.0, 'b'],
               [3, 8.5, 'c']], dtype=object)

        Set `structured=True` to convert to a structured array, which can better
        preserve individual column data such as name and data type.

        >>> df.to_numpy(structured=True)
        array([(1, 6.5, 'a'), (2, 7. , 'b'), (3, 8.5, 'c')],
              dtype=[('foo', 'u1'), ('bar', '<f4'), ('ham', '<U1')])
        """  # noqa: W505
        if use_pyarrow is not None:
            issue_deprecation_warning(
                "The `use_pyarrow` parameter for `DataFrame.to_numpy` is deprecated."
                " Polars now uses its native engine by default for conversion to NumPy.",
                version="0.20.28",
            )

        if structured:
            if not allow_copy and not self.is_empty():
                msg = "copy not allowed: cannot create structured array without copying data"
                raise RuntimeError(msg)

            arrays = []
            struct_dtype = []
            for s in self.iter_columns():
                if s.dtype == Struct:
                    arr = s.struct.unnest().to_numpy(
                        structured=True,
                        allow_copy=True,
                        use_pyarrow=use_pyarrow,
                    )
                else:
                    arr = s.to_numpy(use_pyarrow=use_pyarrow)

                if s.dtype == String and not s.has_nulls():
                    arr = arr.astype(str, copy=False)
                arrays.append(arr)
                struct_dtype.append((s.name, arr.dtype))

            out = np.empty(self.height, dtype=struct_dtype)
            for idx, c in enumerate(self.columns):
                out[c] = arrays[idx]
            return out

        return self._df.to_numpy(order, writable=writable, allow_copy=allow_copy)
