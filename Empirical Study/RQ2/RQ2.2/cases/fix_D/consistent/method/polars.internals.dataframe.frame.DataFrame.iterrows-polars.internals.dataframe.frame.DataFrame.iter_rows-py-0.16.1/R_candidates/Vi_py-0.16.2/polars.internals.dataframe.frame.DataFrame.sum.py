    def sum(
        self: DF,
        *,
        axis: int = 0,
        null_strategy: NullStrategy = "ignore",
    ) -> DF | pli.Series:
        """
        Aggregate the columns of this DataFrame to their sum value.

        Parameters
        ----------
        axis
            Either 0 or 1.
        null_strategy : {'ignore', 'propagate'}
            This argument is only used if axis == 1.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.sum()
        shape: (1, 3)
        ┌─────┬─────┬──────┐
        │ foo ┆ bar ┆ ham  │
        │ --- ┆ --- ┆ ---  │
        │ i64 ┆ i64 ┆ str  │
        ╞═════╪═════╪══════╡
        │ 6   ┆ 21  ┆ null │
        └─────┴─────┴──────┘
        >>> df.sum(axis=1)
        shape: (3,)
        Series: 'foo' [str]
        [
                "16a"
                "27b"
                "38c"
        ]

        """
        if axis == 0:
            return self._from_pydf(self._df.sum())
        if axis == 1:
            return pli.wrap_s(self._df.hsum(null_strategy))
        raise ValueError("Axis should be 0 or 1.")  # pragma: no cover
