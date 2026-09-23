    def max(self) -> Expr:
        """
        Compute the max value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.select(pl.col("values").list.max())
        shape: (2, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ i64    │
        ╞════════╡
        │ 1      │
        │ 3      │
        └────────┘

        """
        return wrap_expr(self._pyexpr.list_max())
