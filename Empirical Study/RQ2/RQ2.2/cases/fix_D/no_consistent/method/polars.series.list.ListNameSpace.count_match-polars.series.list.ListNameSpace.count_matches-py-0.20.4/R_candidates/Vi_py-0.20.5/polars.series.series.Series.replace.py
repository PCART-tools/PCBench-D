    def replace(
        self,
        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
        *,
        default: IntoExpr | NoDefault = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace values by different values.

        Parameters
        ----------
        old
            Value or sequence of values to replace.
            Also accepts a mapping of values to their replacement as syntactic sugar for
            `replace(new=Series(mapping.keys()), old=Series(mapping.values()))`.
        new
            Value or sequence of values to replace by.
            Length must match the length of `old` or have length 1.
        default
            Set values that were not replaced to this value.
            Defaults to keeping the original value.
            Accepts expression input. Non-expression inputs are parsed as literals.
        return_dtype
            The data type of the resulting Series. If set to `None` (default),
            the data type is determined automatically based on the other inputs.

        See Also
        --------
        str.replace

        Notes
        -----
        The global string cache must be enabled when replacing categorical values.

        Examples
        --------
        Replace a single value by another value. Values that were not replaced remain
        unchanged.

        >>> s = pl.Series([1, 2, 2, 3])
        >>> s.replace(2, 100)
        shape: (4,)
        Series: '' [i64]
        [
                1
                100
                100
                3
        ]

        Replace multiple values by passing sequences to the `old` and `new` parameters.

        >>> s.replace([2, 3], [100, 200])
        shape: (4,)
        Series: '' [i64]
        [
                1
                100
                100
                200
        ]

        Passing a mapping with replacements is also supported as syntactic sugar.
        Specify a default to set all values that were not matched.

        >>> mapping = {2: 100, 3: 200}
        >>> s.replace(mapping, default=-1)
        shape: (4,)
        Series: '' [i64]
        [
                -1
                100
                100
                200
        ]


        The default can be another Series.

        >>> default = pl.Series([2.5, 5.0, 7.5, 10.0])
        >>> s.replace(2, 100, default=default)
        shape: (4,)
        Series: '' [f64]
        [
                2.5
                100.0
                100.0
                10.0
        ]

        Replacing by values of a different data type sets the return type based on
        a combination of the `new` data type and either the original data type or the
        default data type if it was set.

        >>> s = pl.Series(["x", "y", "z"])
        >>> mapping = {"x": 1, "y": 2, "z": 3}
        >>> s.replace(mapping)
        shape: (3,)
        Series: '' [str]
        [
                "1"
                "2"
                "3"
        ]
        >>> s.replace(mapping, default=None)
        shape: (3,)
        Series: '' [i64]
        [
                1
                2
                3
        ]

        Set the `return_dtype` parameter to control the resulting data type directly.

        >>> s.replace(mapping, return_dtype=pl.UInt8)
        shape: (3,)
        Series: '' [u8]
        [
                1
                2
                3
        ]
        """
