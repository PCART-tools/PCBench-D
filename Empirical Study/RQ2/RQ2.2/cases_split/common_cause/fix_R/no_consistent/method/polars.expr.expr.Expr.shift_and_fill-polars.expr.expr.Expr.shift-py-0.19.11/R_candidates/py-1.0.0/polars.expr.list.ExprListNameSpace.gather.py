    def gather(
        self,
        indices: Expr | Series | list[int] | list[list[int]],
        *,
        null_on_oob: bool = False,
    ) -> Expr:
        """
        Take sublists by multiple indices.

        The indices may be defined in a single column, or by sublists in another
        column of dtype `List`.

        Parameters
        ----------
        indices
            Indices to return per sublist
        null_on_oob
            Behavior if an index is out of bounds:
            True -> set as null
            False -> raise an error
            Note that defaulting to raising an error is much cheaper

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[3, 2, 1], [], [1, 2, 3, 4, 5]]})
        >>> df.with_columns(gather=pl.col("a").list.gather([0, 4], null_on_oob=True))
        shape: (3, 2)
        ┌─────────────┬──────────────┐
        │ a           ┆ gather       │
        │ ---         ┆ ---          │
        │ list[i64]   ┆ list[i64]    │
        ╞═════════════╪══════════════╡
        │ [3, 2, 1]   ┆ [3, null]    │
        │ []          ┆ [null, null] │
        │ [1, 2, … 5] ┆ [1, 5]       │
        └─────────────┴──────────────┘
        """
        if isinstance(indices, list):
            indices = pl.Series(indices)
        indices = parse_into_expression(indices)
        return wrap_expr(self._pyexpr.list_gather(indices, null_on_oob))
