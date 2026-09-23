    @deprecate_renamed_function("map_elements", version="0.19.0")
    def apply(
        self,
        function: Callable[[Any], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        skip_nulls: bool = True,
    ) -> Self:
        """
        Apply a custom/user-defined function (UDF) over elements in this Series.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`Series.map_elements`.

        Parameters
        ----------
        function
            Custom function or lambda.
        return_dtype
            Output datatype. If none is given, the same datatype as this Series will be
            used.
        skip_nulls
            Nulls will be skipped and not passed to the python function.
            This is faster because python can be skipped and because we call
            more specialized functions.
        """
        return self.map_elements(function, return_dtype, skip_nulls=skip_nulls)
