    def vstack(self, other: DataFrame, *, in_place: bool = False) -> Self:
        """
        Grow this DataFrame vertically by stacking a DataFrame to it.

        Parameters
        ----------
        other
            DataFrame to stack.
        in_place
            Modify in place.

        See Also
        --------
        extend

        Examples
        --------
        >>> df1 = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2],
        ...         "bar": [6, 7],
        ...         "ham": ["a", "b"],
        ...     }
        ... )
        >>> df2 = pl.DataFrame(
        ...     {
        ...         "foo": [3, 4],
        ...         "bar": [8, 9],
        ...         "ham": ["c", "d"],
        ...     }
        ... )
        >>> df1.vstack(df2)
        shape: (4, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6   ┆ a   │
        │ 2   ┆ 7   ┆ b   │
        │ 3   ┆ 8   ┆ c   │
        │ 4   ┆ 9   ┆ d   │
        └─────┴─────┴─────┘

        """
        if in_place:
            try:
                self._df.vstack_mut(other._df)
            except RuntimeError as exc:
                if str(exc) == "Already mutably borrowed":
                    self._df.vstack_mut(other._df.clone())
                    return self
                else:
                    raise
            else:
                return self

        return self._from_pydf(self._df.vstack(other._df))
