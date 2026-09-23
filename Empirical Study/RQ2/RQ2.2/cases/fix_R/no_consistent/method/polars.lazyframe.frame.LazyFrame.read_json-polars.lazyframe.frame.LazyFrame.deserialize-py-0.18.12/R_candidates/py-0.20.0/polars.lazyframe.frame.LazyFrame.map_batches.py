    def map_batches(
        self,
        function: Callable[[DataFrame], DataFrame],
        *,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        slice_pushdown: bool = True,
        no_optimizations: bool = False,
        schema: None | SchemaDict = None,
        validate_output_schema: bool = True,
        streamable: bool = False,
    ) -> Self:
        """
        Apply a custom function.

        It is important that the function returns a Polars DataFrame.

        Parameters
        ----------
        function
            Lambda/ function to apply.
        predicate_pushdown
            Allow predicate pushdown optimization to pass this node.
        projection_pushdown
            Allow projection pushdown optimization to pass this node.
        slice_pushdown
            Allow slice pushdown optimization to pass this node.
        no_optimizations
            Turn off all optimizations past this point.
        schema
            Output schema of the function, if set to `None` we assume that the schema
            will remain unchanged by the applied function.
        validate_output_schema
            It is paramount that polars' schema is correct. This flag will ensure that
            the output schema of this function will be checked with the expected schema.
            Setting this to `False` will not do this check, but may lead to hard to
            debug bugs.
        streamable
            Whether the function that is given is eligible to be running with the
            streaming engine. That means that the function must produce the same result
            when it is executed in batches or when it is be executed on the full
            dataset.

        Warnings
        --------
        The `schema` of a `LazyFrame` must always be correct. It is up to the caller
        of this function to ensure that this invariant is upheld.

        It is important that the optimization flags are correct. If the custom function
        for instance does an aggregation of a column, `predicate_pushdown` should not
        be allowed, as this prunes rows and will influence your aggregation results.

        Examples
        --------
        >>> lf = (  # doctest: +SKIP
        ...     pl.LazyFrame(
        ...         {
        ...             "a": pl.int_range(-100_000, 0, eager=True),
        ...             "b": pl.int_range(0, 100_000, eager=True),
        ...         }
        ...     )
        ...     .map_batches(lambda x: 2 * x, streamable=True)
        ...     .collect(streaming=True)
        ... )
        shape: (100_000, 2)
        ┌─────────┬────────┐
        │ a       ┆ b      │
        │ ---     ┆ ---    │
        │ i64     ┆ i64    │
        ╞═════════╪════════╡
        │ -200000 ┆ 0      │
        │ -199998 ┆ 2      │
        │ -199996 ┆ 4      │
        │ -199994 ┆ 6      │
        │ …       ┆ …      │
        │ -8      ┆ 199992 │
        │ -6      ┆ 199994 │
        │ -4      ┆ 199996 │
        │ -2      ┆ 199998 │
        └─────────┴────────┘

        """
        if no_optimizations:
            predicate_pushdown = False
            projection_pushdown = False
            slice_pushdown = False

        return self._from_pyldf(
            self._ldf.map_batches(
                function,
                predicate_pushdown,
                projection_pushdown,
                slice_pushdown,
                streamable=streamable,
                schema=schema,
                validate_output=validate_output_schema,
            )
        )
