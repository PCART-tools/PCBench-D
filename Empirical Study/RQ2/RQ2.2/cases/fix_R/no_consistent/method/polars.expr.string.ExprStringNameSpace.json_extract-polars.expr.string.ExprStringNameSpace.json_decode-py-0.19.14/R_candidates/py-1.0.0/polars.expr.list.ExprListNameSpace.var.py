    def var(self, ddof: int = 1) -> Expr:
        """
        Compute the var value of the lists in the array.

        Parameters
        ----------
        ddof
            “Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof,
            where N represents the number of elements.
            By default ddof is 1.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[-1, 0, 1], [1, 10]]})
        >>> df.with_columns(pl.col("values").list.var().alias("var"))
        shape: (2, 2)
        ┌────────────┬──────┐
        │ values     ┆ var  │
        │ ---        ┆ ---  │
        │ list[i64]  ┆ f64  │
        ╞════════════╪══════╡
        │ [-1, 0, 1] ┆ 1.0  │
        │ [1, 10]    ┆ 40.5 │
        └────────────┴──────┘
        """
        return wrap_expr(self._pyexpr.list_var(ddof))
