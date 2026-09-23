    def replace_strict(
        self,
        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
        *,
        default: IntoExpr | NoDefault = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace all values by different values.

        Parameters
        ----------
        old
            Value or sequence of values to replace.
            Also accepts a mapping of values to their replacement as syntactic sugar for
            `replace_all(old=Series(mapping.keys()), new=Series(mapping.values()))`.
        new
            Value or sequence of values to replace by.
            Length must match the length of `old` or have length 1.
        default
            Set values that were not replaced to this value. If no default is specified,
            (default), an error is raised if any values were not replaced.
            Accepts expression input. Non-expression inputs are parsed as literals.
        return_dtype
            The data type of the resulting Series. If set to `None` (default),
            the data type is determined automatically based on the other inputs.

        Raises
        ------
        InvalidOperationError
            If any non-null values in the original column were not replaced, and no
            `default` was specified.

        See Also
        --------
        replace
        str.replace

        Notes
        -----
        The global string cache must be enabled when replacing categorical values.

        Examples
        --------
        Replace values by passing sequences to the `old` and `new` parameters.

        >>> s = pl.Series([1, 2, 2, 3])
        >>> s.replace_strict([1, 2, 3], [100, 200, 300])
        shape: (4,)
        Series: '' [i64]
        [
                100
                200
                200
                300
        ]

        Passing a mapping with replacements is also supported as syntactic sugar.

        >>> mapping = {1: 100, 2: 200, 3: 300}
        >>> s.replace_strict(mapping)
        shape: (4,)
        Series: '' [i64]
        [
                100
                200
                200
                300
        ]

        By default, an error is raised if any non-null values were not replaced.
        Specify a default to set all values that were not matched.

        >>> mapping = {2: 200, 3: 300}
        >>> s.replace_strict(mapping)  # doctest: +SKIP
        Traceback (most recent call last):
        ...
        polars.exceptions.InvalidOperationError: incomplete mapping specified for `replace_strict`
        >>> s.replace_strict(mapping, default=-1)
        shape: (4,)
        Series: '' [i64]
        [
                -1
                200
                200
                300
        ]

        The default can be another Series.

        >>> default = pl.Series([2.5, 5.0, 7.5, 10.0])
        >>> s.replace_strict(2, 200, default=default)
        shape: (4,)
        Series: '' [f64]
        [
                2.5
                200.0
                200.0
                10.0
        ]

        Replacing by values of a different data type sets the return type based on
        a combination of the `new` data type and the `default` data type.

        >>> s = pl.Series(["x", "y", "z"])
        >>> mapping = {"x": 1, "y": 2, "z": 3}
        >>> s.replace_strict(mapping)
        shape: (3,)
        Series: '' [i64]
        [
                1
                2
                3
        ]
        >>> s.replace_strict(mapping, default="x")
        shape: (3,)
        Series: '' [str]
        [
                "1"
                "2"
                "3"
        ]

        Set the `return_dtype` parameter to control the resulting data type directly.

        >>> s.replace_strict(mapping, return_dtype=pl.UInt8)
        shape: (3,)
        Series: '' [u8]
        [
                1
                2
                3
        ]
        """  # noqa: W505
