    def sum(
        self,
        *,
        axis: int | None = None,
        null_strategy: NullStrategy = "ignore",
    ) -> Self | Series:
        """
        Aggregate the columns of this DataFrame to their sum value.

        Parameters
        ----------
        axis
            Either 0 (vertical) or 1 (horizontal).

            .. deprecated:: 0.19.14
                This argument will be removed in a future version. This method will only
                support vertical aggregation, as if `axis` were set to `0`.
                To perform horizontal aggregation, use :meth:`sum_horizontal`.
        null_strategy : {'ignore', 'propagate'}
            This argument is only used if `axis == 1`.

            .. deprecated:: 0.19.14
                This argument will be removed in a future version.

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
        """
        if axis is not None:
            issue_deprecation_warning(
                "The `axis` parameter for `DataFrame.sum` is deprecated."
                " Use `DataFrame.sum_horizontal()` to perform horizontal aggregation.",
                version="0.19.14",
            )
        else:
            axis = 0

        if axis == 0:
            return self.lazy().sum().collect(_eager=True)  # type: ignore[return-value]
        if axis == 1:
            if null_strategy == "ignore":
                ignore_nulls = True
            elif null_strategy == "propagate":
                ignore_nulls = False
            else:
                raise ValueError(
                    f"`null_strategy` must be one of {{'ignore', 'propagate'}}, got {null_strategy}"
                )
            return self.sum_horizontal(ignore_nulls=ignore_nulls)
        raise ValueError("axis should be 0 or 1")
