    @unstable()
    def cumulative_eval(
        self, expr: Expr, *, min_periods: int = 1, parallel: bool = False
    ) -> Expr:
        """
        Run an expression over a sliding window that increases `1` slot every iteration.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        expr
            Expression to evaluate
        min_periods
            Number of valid values there should be in the window before the expression
            is evaluated. valid values = `length - null_count`
        parallel
            Run in parallel. Don't do this in a group by or another operation that
            already has much parallelization.

        Warnings
        --------
        This can be really slow as it can have `O(n^2)` complexity. Don't use this
        for operations that visit all elements.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [1, 2, 3, 4, 5]})
        >>> df.select(
        ...     [
        ...         pl.col("values").cumulative_eval(
        ...             pl.element().first() - pl.element().last() ** 2
        ...         )
        ...     ]
        ... )
        shape: (5, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ i64    │
        ╞════════╡
        │ 0      │
        │ -3     │
        │ -8     │
        │ -15    │
        │ -24    │
        └────────┘
        """
        return self._from_pyexpr(
            self._pyexpr.cumulative_eval(expr._pyexpr, min_periods, parallel)
        )
