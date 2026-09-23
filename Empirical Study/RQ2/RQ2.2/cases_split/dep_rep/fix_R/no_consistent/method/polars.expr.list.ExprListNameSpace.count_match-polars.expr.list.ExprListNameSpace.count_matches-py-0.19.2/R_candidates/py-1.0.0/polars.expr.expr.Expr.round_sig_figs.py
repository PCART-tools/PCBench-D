    def round_sig_figs(self, digits: int) -> Expr:
        """
        Round to a number of significant figures.

        Parameters
        ----------
        digits
            Number of significant figures to round to.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [0.01234, 3.333, 1234.0]})
        >>> df.with_columns(pl.col("a").round_sig_figs(2).alias("round_sig_figs"))
        shape: (3, 2)
        ┌─────────┬────────────────┐
        │ a       ┆ round_sig_figs │
        │ ---     ┆ ---            │
        │ f64     ┆ f64            │
        ╞═════════╪════════════════╡
        │ 0.01234 ┆ 0.012          │
        │ 3.333   ┆ 3.3            │
        │ 1234.0  ┆ 1200.0         │
        └─────────┴────────────────┘
        """
        return self._from_pyexpr(self._pyexpr.round_sig_figs(digits))
