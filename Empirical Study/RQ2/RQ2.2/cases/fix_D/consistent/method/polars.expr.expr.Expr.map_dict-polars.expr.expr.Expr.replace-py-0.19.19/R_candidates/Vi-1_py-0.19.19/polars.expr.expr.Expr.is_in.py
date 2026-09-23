    def is_in(self, other: Expr | Collection[Any] | Series) -> Self:
        """
        Check if elements of this expression are present in the other Series.

        Parameters
        ----------
        other
            Series or sequence of primitive type.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"sets": [[1, 2, 3], [1, 2], [9, 10]], "optional_members": [1, 2, 3]}
        ... )
        >>> df.with_columns(contains=pl.col("optional_members").is_in("sets"))
        shape: (3, 3)
        ┌───────────┬──────────────────┬──────────┐
        │ sets      ┆ optional_members ┆ contains │
        │ ---       ┆ ---              ┆ ---      │
        │ list[i64] ┆ i64              ┆ bool     │
        ╞═══════════╪══════════════════╪══════════╡
        │ [1, 2, 3] ┆ 1                ┆ true     │
        │ [1, 2]    ┆ 2                ┆ true     │
        │ [9, 10]   ┆ 3                ┆ false    │
        └───────────┴──────────────────┴──────────┘

        """
        if isinstance(other, Collection) and not isinstance(other, str):
            if isinstance(other, (Set, FrozenSet)):
                other = list(other)
            implied_dtype = Null if len(other) == 0 else None
            other = F.lit(pl.Series(other, dtype=implied_dtype))._pyexpr
        else:
            other = parse_as_expression(other)
        return self._from_pyexpr(self._pyexpr.is_in(other))
