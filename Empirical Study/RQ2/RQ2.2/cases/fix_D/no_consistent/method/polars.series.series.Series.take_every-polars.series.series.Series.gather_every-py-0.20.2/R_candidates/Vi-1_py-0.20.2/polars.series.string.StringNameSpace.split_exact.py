    def split_exact(self, by: IntoExpr, n: int, *, inclusive: bool = False) -> Series:
        """
        Split the string by a substring using `n` splits.

        Results in a struct of `n+1` fields.

        If it cannot make `n` splits, the remaining field elements will be null.

        Parameters
        ----------
        by
            Substring to split by.
        n
            Number of splits to make.
        inclusive
            If True, include the split character/string in the results.

        Examples
        --------
        >>> df = pl.DataFrame({"x": ["a_1", None, "c", "d_4"]})
        >>> df["x"].str.split_exact("_", 1).alias("fields")
        shape: (4,)
        Series: 'fields' [struct[2]]
        [
                {"a","1"}
                {null,null}
                {"c",null}
                {"d","4"}
        ]

        Split string values in column x in exactly 2 parts and assign
        each part to a new column.

        >>> (
        ...     df["x"]
        ...     .str.split_exact("_", 1)
        ...     .struct.rename_fields(["first_part", "second_part"])
        ...     .alias("fields")
        ...     .to_frame()
        ...     .unnest("fields")
        ... )
        shape: (4, 2)
        ┌────────────┬─────────────┐
        │ first_part ┆ second_part │
        │ ---        ┆ ---         │
        │ str        ┆ str         │
        ╞════════════╪═════════════╡
        │ a          ┆ 1           │
        │ null       ┆ null        │
        │ c          ┆ null        │
        │ d          ┆ 4           │
        └────────────┴─────────────┘

        Returns
        -------
        Series
            Series of data type :class:`Struct` with fields of data type :class:`Utf8`.

        """
