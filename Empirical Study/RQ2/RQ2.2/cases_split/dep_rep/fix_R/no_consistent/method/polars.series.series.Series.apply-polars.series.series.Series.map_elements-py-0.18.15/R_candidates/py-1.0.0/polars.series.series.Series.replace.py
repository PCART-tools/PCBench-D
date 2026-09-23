    def replace(
        self,
        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
        *,
        default: IntoExpr | NoDefault = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace values by different values of the same data type.

        Parameters
        ----------
        old
            Value or sequence of values to replace.
            Also accepts a mapping of values to their replacement as syntactic sugar for
            `replace(old=Series(mapping.keys()), new=Series(mapping.values()))`.
        new
            Value or sequence of values to replace by.
            Length must match the length of `old` or have length 1.

        default
            Set values that were not replaced to this value.
            Defaults to keeping the original value.
            Accepts expression input. Non-expression inputs are parsed as literals.

            .. deprecated:: 0.20.31
                Use :meth:`replace_all` instead to set a default while replacing values.

        return_dtype
            The data type of the resulting expression. If set to `None` (default),
            the data type is determined automatically based on the other inputs.

            .. deprecated:: 0.20.31
                Use :meth:`replace_all` instead to set a return data type while
                replacing values.


        See Also
        --------
        replace_strict
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

        >>> mapping = {2: 100, 3: 200}
        >>> s.replace(mapping)
        shape: (4,)
        Series: '' [i64]
        [
                1
                100
                100
                200
        ]

        The original data type is preserved when replacing by values of a different
        data type. Use :meth:`replace_strict` to replace and change the return data
        type.

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
        """
