    def clear(self, n: int = 0) -> DataFrame:
        """
        Create an empty (n=0) or `n`-row null-filled (n>0) copy of the DataFrame.

        Returns a `n`-row null-filled DataFrame with an identical schema.
        `n` can be greater than the current number of rows in the DataFrame.

        Parameters
        ----------
        n
            Number of (null-filled) rows to return in the cleared frame.

        See Also
        --------
        clone : Cheap deepcopy/clone.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [None, 2, 3, 4],
        ...         "b": [0.5, None, 2.5, 13],
        ...         "c": [True, True, False, None],
        ...     }
        ... )
        >>> df.clear()
        shape: (0, 3)
        ┌─────┬─────┬──────┐
        │ a   ┆ b   ┆ c    │
        │ --- ┆ --- ┆ ---  │
        │ i64 ┆ f64 ┆ bool │
        ╞═════╪═════╪══════╡
        └─────┴─────┴──────┘

        >>> df.clear(n=2)
        shape: (2, 3)
        ┌──────┬──────┬──────┐
        │ a    ┆ b    ┆ c    │
        │ ---  ┆ ---  ┆ ---  │
        │ i64  ┆ f64  ┆ bool │
        ╞══════╪══════╪══════╡
        │ null ┆ null ┆ null │
        │ null ┆ null ┆ null │
        └──────┴──────┴──────┘
        """
        if n < 0:
            msg = f"`n` should be greater than or equal to 0, got {n}"
            raise ValueError(msg)
        # faster path
        if n == 0:
            return self._from_pydf(self._df.clear())
        return self.__class__(
            {
                nm: pl.Series(name=nm, dtype=tp).extend_constant(None, n)
                for nm, tp in self.schema.items()
            }
        )
