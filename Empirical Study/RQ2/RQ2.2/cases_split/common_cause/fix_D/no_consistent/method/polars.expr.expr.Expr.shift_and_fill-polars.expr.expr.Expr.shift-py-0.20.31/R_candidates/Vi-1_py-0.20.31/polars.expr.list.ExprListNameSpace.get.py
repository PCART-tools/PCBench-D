    def get(
        self,
        index: int | Expr | str,
        *,
        null_on_oob: bool = True,
    ) -> Expr:
        """
        Get the value by index in the sublists.

        So index `0` would return the first item of every sublist
        and index `-1` would return the last item of every sublist
        if an index is out of bounds, it will return a `None`.

        Parameters
        ----------
        index
            Index to return per sublist
        null_on_oob
            Behavior if an index is out of bounds:
            True -> set as null
            False -> raise an error

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[3, 2, 1], [], [1, 2]]})
        >>> df.with_columns(get=pl.col("a").list.get(0))
        shape: (3, 2)
        ┌───────────┬──────┐
        │ a         ┆ get  │
        │ ---       ┆ ---  │
        │ list[i64] ┆ i64  │
        ╞═══════════╪══════╡
        │ [3, 2, 1] ┆ 3    │
        │ []        ┆ null │
        │ [1, 2]    ┆ 1    │
        └───────────┴──────┘
        """
        index = parse_as_expression(index)
        return wrap_expr(self._pyexpr.list_get(index, null_on_oob))
