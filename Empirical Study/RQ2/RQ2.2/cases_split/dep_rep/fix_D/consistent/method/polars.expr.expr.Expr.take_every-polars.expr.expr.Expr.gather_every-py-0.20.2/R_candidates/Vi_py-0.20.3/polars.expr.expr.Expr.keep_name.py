    @deprecate_renamed_function("name.keep", moved=True, version="0.19.12")
    def keep_name(self) -> Self:
        """
        Keep the original root name of the expression.

        .. deprecated:: 0.19.12
            This method has been renamed to :func:`name.keep`.

        Notes
        -----
        Due to implementation constraints, this method can only be called as the last
        expression in a chain.

        See Also
        --------
        alias

        Examples
        --------
        Undo an alias operation.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2],
        ...         "b": [3, 4],
        ...     }
        ... )
        >>> df.with_columns((pl.col("a") * 9).alias("c").name.keep())
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 9   ┆ 3   │
        │ 18  ┆ 4   │
        └─────┴─────┘

        Prevent errors due to duplicate column names.

        >>> df.select((pl.lit(10) / pl.all()).name.keep())
        shape: (2, 2)
        ┌──────┬──────────┐
        │ a    ┆ b        │
        │ ---  ┆ ---      │
        │ f64  ┆ f64      │
        ╞══════╪══════════╡
        │ 10.0 ┆ 3.333333 │
        │ 5.0  ┆ 2.5      │
        └──────┴──────────┘

        """
        return self.name.keep()  # type: ignore[return-value]
