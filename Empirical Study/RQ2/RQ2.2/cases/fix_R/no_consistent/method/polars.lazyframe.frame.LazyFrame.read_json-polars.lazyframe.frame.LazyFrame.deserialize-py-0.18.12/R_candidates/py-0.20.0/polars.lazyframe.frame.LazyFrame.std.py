    def std(self, ddof: int = 1) -> Self:
        """
        Aggregate the columns in the LazyFrame to their standard deviation value.

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
        >>> lf.std().collect()
        shape: (1, 2)
        ┌──────────┬─────┐
        │ a        ┆ b   │
        │ ---      ┆ --- │
        │ f64      ┆ f64 │
        ╞══════════╪═════╡
        │ 1.290994 ┆ 0.5 │
        └──────────┴─────┘
        >>> lf.std(ddof=0).collect()
        shape: (1, 2)
        ┌──────────┬──────────┐
        │ a        ┆ b        │
        │ ---      ┆ ---      │
        │ f64      ┆ f64      │
        ╞══════════╪══════════╡
        │ 1.118034 ┆ 0.433013 │
        └──────────┴──────────┘

        """
        return self._from_pyldf(self._ldf.std(ddof))
