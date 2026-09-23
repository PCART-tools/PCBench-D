    def var(self, ddof: int = 1) -> LazyFrame:
        """
        Aggregate the columns in the LazyFrame to their variance value.

        Parameters
        ----------
        ddof
            “Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof,
            where N represents the number of elements.
            By default ddof is 1.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [1, 2, 1, 1],
        ...     }
        ... )
        >>> lf.var().collect()
        shape: (1, 2)
        ┌──────────┬──────┐
        │ a        ┆ b    │
        │ ---      ┆ ---  │
        │ f64      ┆ f64  │
        ╞══════════╪══════╡
        │ 1.666667 ┆ 0.25 │
        └──────────┴──────┘
        >>> lf.var(ddof=0).collect()
        shape: (1, 2)
        ┌──────┬────────┐
        │ a    ┆ b      │
        │ ---  ┆ ---    │
        │ f64  ┆ f64    │
        ╞══════╪════════╡
        │ 1.25 ┆ 0.1875 │
        └──────┴────────┘
        """
        return self._from_pyldf(self._ldf.var(ddof))
