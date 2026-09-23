    @deprecate_renamed_function("map_rows", version="0.19.0")
    def apply(
        self,
        function: Callable[[tuple[Any, ...]], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        inference_size: int = 256,
    ) -> DataFrame:
        """
        Apply a custom/user-defined function (UDF) over the rows of the DataFrame.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`DataFrame.map_rows`.

        Parameters
        ----------
        function
            Custom function or lambda.
        return_dtype
            Output type of the operation. If none given, Polars tries to infer the type.
        inference_size
            Only used in the case when the custom function returns rows.
            This uses the first `n` rows to determine the output schema

        """
        return self.map_rows(function, return_dtype, inference_size=inference_size)
