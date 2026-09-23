    def sample(
        self,
        n: int | Series | None = None,
        *,
        fraction: float | Series | None = None,
        with_replacement: bool = False,
        shuffle: bool = False,
        seed: int | None = None,
    ) -> DataFrame:
        """
        Sample from this DataFrame.

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
            If set to True, the order of the sampled rows will be shuffled. If
            set to False (default), the order of the returned rows will be
            neither stable nor fully random.
        seed
            Seed for the random number generator. If set to None (default), a
            random seed is generated for each sample operation.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.sample(n=2, seed=0)  # doctest: +IGNORE_RESULT
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 3   ┆ 8   ┆ c   │
        │ 2   ┆ 7   ┆ b   │
        └─────┴─────┴─────┘
        """
        if n is not None and fraction is not None:
            msg = "cannot specify both `n` and `fraction`"
            raise ValueError(msg)

        if seed is None:
            seed = random.randint(0, 10000)

        if n is None and fraction is not None:
            if not isinstance(fraction, pl.Series):
                fraction = pl.Series("frac", [fraction])

            return self._from_pydf(
                self._df.sample_frac(fraction._s, with_replacement, shuffle, seed)
            )

        if n is None:
            n = 1

        if not isinstance(n, pl.Series):
            n = pl.Series("", [n])

        return self._from_pydf(self._df.sample_n(n._s, with_replacement, shuffle, seed))
