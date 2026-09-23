    def mean(
        self,
        *,
        axis: int | None = None,
        null_strategy: NullStrategy = "ignore",
    ) -> Self | Series:
        """
        Aggregate the columns of this DataFrame to their mean value.

        Parameters
        ----------
        axis
            Either 0 (vertical) or 1 (horizontal).

            .. deprecated:: 0.19.14
                This argument will be removed in a future version. This method will only
                support vertical aggregation, as if `axis` were set to `0`.
                To perform horizontal aggregation, use :meth:`mean_horizontal`.
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
        ...         "spam": [True, False, None],
        ...     }
        ... )
        >>> df.mean()
        shape: (1, 4)
        ┌─────┬─────┬──────┬──────┐
        │ foo ┆ bar ┆ ham  ┆ spam │
        │ --- ┆ --- ┆ ---  ┆ ---  │
        │ f64 ┆ f64 ┆ str  ┆ f64  │
        ╞═════╪═════╪══════╪══════╡
        │ 2.0 ┆ 7.0 ┆ null ┆ 0.5  │
        └─────┴─────┴──────┴──────┘
        """
        if axis is not None:
            issue_deprecation_warning(
                "The `axis` parameter for `DataFrame.mean` is deprecated."
                " Use `DataFrame.mean_horizontal()` to perform horizontal aggregation.",
                version="0.19.14",
            )
        else:
            axis = 0

        if axis == 0:
            return self.lazy().mean().collect(_eager=True)  # type: ignore[return-value]
        if axis == 1:
            if null_strategy == "ignore":
                ignore_nulls = True
            elif null_strategy == "propagate":
                ignore_nulls = False
            else:
                raise ValueError(
                    f"`null_strategy` must be one of {{'ignore', 'propagate'}}, got {null_strategy}"
                )
            return self.mean_horizontal(ignore_nulls=ignore_nulls)
        raise ValueError("axis should be 0 or 1")
