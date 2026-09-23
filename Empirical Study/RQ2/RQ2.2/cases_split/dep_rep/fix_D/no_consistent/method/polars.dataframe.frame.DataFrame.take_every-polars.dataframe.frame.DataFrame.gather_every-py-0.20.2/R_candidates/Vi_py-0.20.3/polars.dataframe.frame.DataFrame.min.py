    def min(self, axis: int | None = None) -> Self | Series:
        """
        Aggregate the columns of this DataFrame to their minimum value.

        Parameters
        ----------
        axis
            Either 0 (vertical) or 1 (horizontal).

            .. deprecated:: 0.19.14
                This argument will be removed in a future version. This method will only
                support vertical aggregation, as if `axis` were set to `0`.
                To perform horizontal aggregation, use :meth:`min_horizontal`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.min()
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6   ┆ a   │
        └─────┴─────┴─────┘

        """
        if axis is not None:
            issue_deprecation_warning(
                "The `axis` parameter for `DataFrame.min` is deprecated."
                " Use `DataFrame.min_horizontal()` to perform horizontal aggregation.",
                version="0.19.14",
            )
        else:
            axis = 0

        if axis == 0:
            return self.lazy().min().collect(_eager=True)  # type: ignore[return-value]
        if axis == 1:
            return wrap_s(self._df.min_horizontal())
        raise ValueError("axis should be 0 or 1")
