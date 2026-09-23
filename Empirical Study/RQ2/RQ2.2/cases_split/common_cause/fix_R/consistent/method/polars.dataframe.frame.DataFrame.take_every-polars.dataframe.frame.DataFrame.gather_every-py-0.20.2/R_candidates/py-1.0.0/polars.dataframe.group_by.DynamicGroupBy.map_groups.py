    def map_groups(
        self,
        function: Callable[[DataFrame], DataFrame],
        schema: SchemaDict | None,
    ) -> DataFrame:
        """
        Apply a custom/user-defined function (UDF) over the groups as a new DataFrame.

        Using this is considered an anti-pattern as it will be very slow because:

        - it forces the engine to materialize the whole `DataFrames` for the groups.
        - it is not parallelized.
        - it blocks optimizations as the passed python function is opaque to the
          optimizer.

        The idiomatic way to apply custom functions over multiple columns is using:

        `pl.struct([my_columns]).map_elements(lambda struct_series: ..)`

        Parameters
        ----------
        function
            Function to apply over each group of the `LazyFrame`; it receives
            a DataFrame and should return a DataFrame.
        schema
            Schema of the output function. This has to be known statically. If the
            given schema is incorrect, this is a bug in the caller's query and may
            lead to errors. If set to None, polars assumes the schema is unchanged.
        """
        return (
            self.df.lazy()
            .group_by_dynamic(
                index_column=self.time_column,
                every=self.every,
                period=self.period,
                offset=self.offset,
                include_boundaries=self.include_boundaries,
                closed=self.closed,
                group_by=self.group_by,
                start_by=self.start_by,
            )
            .map_groups(function, schema)
            .collect(no_optimization=True)
        )
