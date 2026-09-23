    def get(self, index: int | IntoExprColumn, *, null_on_oob: bool = False) -> Expr:
        """
        Get the value by index in the sub-arrays.

        So index `0` would return the first item of every sublist
        and index `-1` would return the last item of every sublist
        if an index is out of bounds, it will return a `None`.

        Parameters
        ----------
        index
            Index to return per sub-array
        null_on_oob
            Behavior if an index is out of bounds:
            True -> set as null
            False -> raise an error

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"arr": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "idx": [1, -2, 0]},
        ...     schema={"arr": pl.Array(pl.Int32, 3), "idx": pl.Int32},
        ... )
        >>> df.with_columns(get=pl.col("arr").arr.get("idx", null_on_oob=True))
        shape: (3, 3)
        ┌───────────────┬─────┬─────┐
        │ arr           ┆ idx ┆ get │
        │ ---           ┆ --- ┆ --- │
        │ array[i32, 3] ┆ i32 ┆ i32 │
        ╞═══════════════╪═════╪═════╡
        │ [1, 2, 3]     ┆ 1   ┆ 2   │
        │ [4, 5, 6]     ┆ -2  ┆ 5   │
        │ [7, 8, 9]     ┆ 0   ┆ 7   │
        └───────────────┴─────┴─────┘

        """
        index = parse_into_expression(index)
        return wrap_expr(self._pyexpr.arr_get(index, null_on_oob))
