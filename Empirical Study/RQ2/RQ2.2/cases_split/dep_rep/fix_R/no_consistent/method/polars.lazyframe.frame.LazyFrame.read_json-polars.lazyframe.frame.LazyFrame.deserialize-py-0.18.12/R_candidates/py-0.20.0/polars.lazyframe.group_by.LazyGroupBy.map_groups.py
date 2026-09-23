    def map_groups(
        self,
        function: Callable[[DataFrame], DataFrame],
        schema: SchemaDict | None,
    ) -> LazyFrame:
        """
        Apply a custom/user-defined function (UDF) over the groups as a new DataFrame.

        .. warning::
            This method is much slower than the native expressions API.
            Only use it if you cannot implement your logic otherwise.

        Using this is considered an anti-pattern as it will be very slow because:

        - it forces the engine to materialize the whole `DataFrames` for the groups.
        - it is not parallelized
        - it blocks optimizations as the passed python function is opaque to the
          optimizer

        The idiomatic way to apply custom functions over multiple columns is using:

        `pl.struct([my_columns]).apply(lambda struct_series: ..)`

        Parameters
        ----------
        function
            Function to apply over each group of the `LazyFrame`.
        schema
            Schema of the output function. This has to be known statically. If the
            given schema is incorrect, this is a bug in the caller's query and may
            lead to errors. If set to None, polars assumes the schema is unchanged.

        Examples
        --------
        For each color group sample two rows:

        >>> df = pl.DataFrame(
        ...     {
        ...         "id": [0, 1, 2, 3, 4],
        ...         "color": ["red", "green", "green", "red", "red"],
        ...         "shape": ["square", "triangle", "square", "triangle", "square"],
        ...     }
        ... )
        >>> (
        ...     df.lazy()
        ...     .group_by("color")
        ...     .map_groups(lambda group_df: group_df.sample(2), schema=None)
        ...     .collect()
        ... )  # doctest: +IGNORE_RESULT
        shape: (4, 3)
        ┌─────┬───────┬──────────┐
        │ id  ┆ color ┆ shape    │
        │ --- ┆ ---   ┆ ---      │
        │ i64 ┆ str   ┆ str      │
        ╞═════╪═══════╪══════════╡
        │ 1   ┆ green ┆ triangle │
        │ 2   ┆ green ┆ square   │
        │ 4   ┆ red   ┆ square   │
        │ 3   ┆ red   ┆ triangle │
        └─────┴───────┴──────────┘

        It is better to implement this with an expression:

        >>> (
        ...     df.lazy()
        ...     .filter(pl.int_range(0, pl.count()).shuffle().over("color") < 2)
        ...     .collect()
        ... )  # doctest: +IGNORE_RESULT

        """
        return wrap_ldf(self.lgb.map_groups(function, schema))
