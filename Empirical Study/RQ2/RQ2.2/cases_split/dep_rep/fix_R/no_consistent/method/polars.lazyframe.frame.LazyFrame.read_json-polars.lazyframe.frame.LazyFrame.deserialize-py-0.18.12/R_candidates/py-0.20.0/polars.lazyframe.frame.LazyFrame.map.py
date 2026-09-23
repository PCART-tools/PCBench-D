    @deprecate_renamed_function("map_batches", version="0.19.0")
    def map(
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

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`LazyFrame.map_batches`.

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

        """
        return self.map_batches(
            function,
            predicate_pushdown=predicate_pushdown,
            projection_pushdown=projection_pushdown,
            slice_pushdown=slice_pushdown,
            no_optimizations=no_optimizations,
            schema=schema,
            validate_output_schema=validate_output_schema,
            streamable=streamable,
        )
