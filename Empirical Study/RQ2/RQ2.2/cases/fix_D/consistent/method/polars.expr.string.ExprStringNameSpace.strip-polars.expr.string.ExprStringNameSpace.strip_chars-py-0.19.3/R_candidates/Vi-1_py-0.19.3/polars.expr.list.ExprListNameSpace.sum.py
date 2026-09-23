    def sum(self) -> Expr:
        """
        Sum all the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.select(pl.col("values").list.sum())
        shape: (2, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ i64    │
        ╞════════╡
        │ 1      │
        │ 5      │
        └────────┘

        """
        return wrap_expr(self._pyexpr.list_sum())
