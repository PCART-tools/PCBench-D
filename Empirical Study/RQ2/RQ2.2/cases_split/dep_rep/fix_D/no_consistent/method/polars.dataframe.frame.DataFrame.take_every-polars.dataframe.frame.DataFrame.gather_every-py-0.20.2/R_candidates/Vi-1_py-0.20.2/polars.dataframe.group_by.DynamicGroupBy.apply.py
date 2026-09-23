    @deprecate_renamed_function("map_groups", version="0.19.0")
    def apply(
        self,
        function: Callable[[DataFrame], DataFrame],
        schema: SchemaDict | None,
    ) -> DataFrame:
        """
        Apply a custom/user-defined function (UDF) over the groups as a new DataFrame.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`DynamicGroupBy.map_groups`.

        Parameters
        ----------
        function
            Function to apply over each group of the `LazyFrame`.
        schema
            Schema of the output function. This has to be known statically. If the
            given schema is incorrect, this is a bug in the caller's query and may
            lead to errors. If set to None, polars assumes the schema is unchanged.

        """
        return self.map_groups(function, schema)
