    def eval(self, expr: Expr, *, parallel: bool = False) -> Series:
        """
        Run any polars expression against the lists' elements.

        Parameters
        ----------
        expr
            Expression to run. Note that you can select an element with `pl.first()`, or
            `pl.col()`
        parallel
            Run all expression parallel. Don't activate this blindly.
            Parallelism is worth it if there is enough work to do per thread.

            This likely should not be use in the group by context, because we already
            parallel execution per group

        Examples
        --------
        >>> s = pl.Series("a", [[1, 4], [8, 5], [3, 2]])
        >>> s.list.eval(pl.element().rank())
        shape: (3,)
        Series: 'a' [list[f64]]
        [
            [1.0, 2.0]
            [2.0, 1.0]
            [2.0, 1.0]
        ]
        """
