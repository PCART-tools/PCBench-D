    def min(self) -> Expr:
        """
        Compute the min value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.select(pl.col("values").list.min())
        shape: (2, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ i64    │
        ╞════════╡
        │ 1      │
        │ 2      │
        └────────┘

        """
        return wrap_expr(self._pyexpr.list_min())
