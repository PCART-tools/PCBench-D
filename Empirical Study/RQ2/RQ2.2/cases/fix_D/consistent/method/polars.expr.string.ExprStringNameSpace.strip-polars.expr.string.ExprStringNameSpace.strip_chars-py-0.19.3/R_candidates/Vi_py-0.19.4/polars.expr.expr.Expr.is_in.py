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
        >>> df.select([pl.col("optional_members").is_in("sets").alias("contains")])
        shape: (3, 1)
        ┌──────────┐
        │ contains │
        │ ---      │
        │ bool     │
        ╞══════════╡
        │ true     │
        │ true     │
        │ false    │
        └──────────┘

        """
        if isinstance(other, Collection) and not isinstance(other, str):
            if isinstance(other, (Set, FrozenSet)):
                other = list(other)
            other = F.lit(pl.Series(other))
            other = other._pyexpr
        else:
            other = parse_as_expression(other)
        return self._from_pyexpr(self._pyexpr.is_in(other))
