    def mean(self) -> Expr:
        """
        Compute the mean value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.select(pl.col("values").list.mean())
        shape: (2, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ f64    │
        ╞════════╡
        │ 1.0    │
        │ 2.5    │
        └────────┘

        """
        return wrap_expr(self._pyexpr.list_mean())
