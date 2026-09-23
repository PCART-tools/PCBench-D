    @deprecate_renamed_function("map_batches", version="0.19.0")
    def map(
        self,
        function: Callable[[Series], Series | Any],
        return_dtype: PolarsDataType | None = None,
        *,
        agg_list: bool = False,
    ) -> Self:
        """
        Apply a custom python function to a Series or sequence of Series.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`Expr.map_batches`.

        Parameters
        ----------
        function
            Lambda/ function to apply.
        return_dtype
            Dtype of the output Series.
        agg_list
            Aggregate list
        """
        return self.map_batches(function, return_dtype, agg_list=agg_list)
