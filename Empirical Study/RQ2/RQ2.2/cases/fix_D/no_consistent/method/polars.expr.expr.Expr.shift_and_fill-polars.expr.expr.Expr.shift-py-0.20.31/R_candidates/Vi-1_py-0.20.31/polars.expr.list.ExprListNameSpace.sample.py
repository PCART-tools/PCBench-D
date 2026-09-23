    def sample(
        self,
        n: int | IntoExprColumn | None = None,
        *,
        fraction: float | IntoExprColumn | None = None,
        with_replacement: bool = False,
        shuffle: bool = False,
        seed: int | None = None,
    ) -> Expr:
        """
        Sample from this list.

        Parameters
        ----------
        n
            Number of items to return. Cannot be used with `fraction`. Defaults to 1 if
            `fraction` is None.
        fraction
            Fraction of items to return. Cannot be used with `n`.
        with_replacement
            Allow values to be sampled more than once.
        shuffle
            Shuffle the order of sampled data points.
        seed
            Seed for the random number generator. If set to None (default), a
            random seed is generated for each sample operation.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1, 2, 3], [4, 5]], "n": [2, 1]})
        >>> df.with_columns(sample=pl.col("values").list.sample(n=pl.col("n"), seed=1))
        shape: (2, 3)
        ┌───────────┬─────┬───────────┐
        │ values    ┆ n   ┆ sample    │
        │ ---       ┆ --- ┆ ---       │
        │ list[i64] ┆ i64 ┆ list[i64] │
        ╞═══════════╪═════╪═══════════╡
        │ [1, 2, 3] ┆ 2   ┆ [2, 1]    │
        │ [4, 5]    ┆ 1   ┆ [5]       │
        └───────────┴─────┴───────────┘
        """
        if n is not None and fraction is not None:
            msg = "cannot specify both `n` and `fraction`"
            raise ValueError(msg)

        if fraction is not None:
            fraction = parse_as_expression(fraction)
            return wrap_expr(
                self._pyexpr.list_sample_fraction(
                    fraction, with_replacement, shuffle, seed
                )
            )

        if n is None:
            n = 1
        n = parse_as_expression(n)
        return wrap_expr(self._pyexpr.list_sample_n(n, with_replacement, shuffle, seed))
