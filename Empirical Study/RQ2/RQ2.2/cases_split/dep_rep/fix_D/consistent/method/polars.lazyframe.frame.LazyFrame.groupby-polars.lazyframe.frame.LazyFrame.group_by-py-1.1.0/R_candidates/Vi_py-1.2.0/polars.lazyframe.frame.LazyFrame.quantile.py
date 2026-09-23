    def quantile(
        self,
        quantile: float | Expr,
        interpolation: RollingInterpolationMethod = "nearest",
    ) -> LazyFrame:
        """
        Aggregate the columns in the LazyFrame to their quantile value.

        Parameters
        ----------
        quantile
            Quantile between 0.0 and 1.0.
        interpolation : {'nearest', 'higher', 'lower', 'midpoint', 'linear'}
            Interpolation method.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [1, 2, 1, 1],
        ...     }
        ... )
        >>> lf.quantile(0.7).collect()
        shape: (1, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ f64 ┆ f64 │
        ╞═════╪═════╡
        │ 3.0 ┆ 1.0 │
        └─────┴─────┘
        """
        quantile = parse_into_expression(quantile)
        return self._from_pyldf(self._ldf.quantile(quantile, interpolation))
