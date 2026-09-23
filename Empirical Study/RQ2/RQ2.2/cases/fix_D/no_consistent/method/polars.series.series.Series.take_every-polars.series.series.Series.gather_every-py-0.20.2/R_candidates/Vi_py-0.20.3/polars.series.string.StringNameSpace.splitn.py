    def splitn(self, by: IntoExpr, n: int) -> Series:
        """
        Split the string by a substring, restricted to returning at most `n` items.

        If the number of possible splits is less than `n-1`, the remaining field
        elements will be null. If the number of possible splits is `n-1` or greater,
        the last (nth) substring will contain the remainder of the string.

        Parameters
        ----------
        by
            Substring to split by.
        n
            Max number of items to return.

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["foo bar", None, "foo-bar", "foo bar baz"]})
        >>> df["s"].str.splitn(" ", 2).alias("fields")
        shape: (4,)
        Series: 'fields' [struct[2]]
        [
                {"foo","bar"}
                {null,null}
                {"foo-bar",null}
                {"foo","bar baz"}
        ]

        Split string values in column s in exactly 2 parts and assign
        each part to a new column.

        >>> (
        ...     df["s"]
        ...     .str.splitn(" ", 2)
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
        │ foo        ┆ bar         │
        │ null       ┆ null        │
        │ foo-bar    ┆ null        │
        │ foo        ┆ bar baz     │
        └────────────┴─────────────┘

        Returns
        -------
        Series
            Series of data type :class:`Struct` with fields of data type
            :class:`String`.

        """
