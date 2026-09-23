    def split_exact(self, by: IntoExpr, n: int, *, inclusive: bool = False) -> Expr:
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

        Returns
        -------
        Expr
            Expression of data type :class:`Struct` with fields of data type
            :class:`Utf8`.

        Examples
        --------
        >>> df = pl.DataFrame({"x": ["a_1", None, "c", "d_4"]})
        >>> df.with_columns(
        ...     extracted=pl.col("x").str.split_exact("_", 1).alias("fields"),
        ... )
        shape: (4, 2)
        ┌──────┬─────────────┐
        │ x    ┆ extracted   │
        │ ---  ┆ ---         │
        │ str  ┆ struct[2]   │
        ╞══════╪═════════════╡
        │ a_1  ┆ {"a","1"}   │
        │ null ┆ {null,null} │
        │ c    ┆ {"c",null}  │
        │ d_4  ┆ {"d","4"}   │
        └──────┴─────────────┘


        Split string values in column x in exactly 2 parts and assign
        each part to a new column.

        >>> df.with_columns(
        ...     [
        ...         pl.col("x")
        ...         .str.split_exact("_", 1)
        ...         .struct.rename_fields(["first_part", "second_part"])
        ...         .alias("fields"),
        ...     ]
        ... ).unnest("fields")
        shape: (4, 3)
        ┌──────┬────────────┬─────────────┐
        │ x    ┆ first_part ┆ second_part │
        │ ---  ┆ ---        ┆ ---         │
        │ str  ┆ str        ┆ str         │
        ╞══════╪════════════╪═════════════╡
        │ a_1  ┆ a          ┆ 1           │
        │ null ┆ null       ┆ null        │
        │ c    ┆ c          ┆ null        │
        │ d_4  ┆ d          ┆ 4           │
        └──────┴────────────┴─────────────┘

        """
        by = parse_as_expression(by, str_as_lit=True)
        if inclusive:
            return wrap_expr(self._pyexpr.str_split_exact_inclusive(by, n))
        return wrap_expr(self._pyexpr.str_split_exact(by, n))
