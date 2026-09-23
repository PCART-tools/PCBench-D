    @deprecate_renamed_function("map_elements", version="0.19.0")
    def apply(
        self,
        function: Callable[[Series], Series] | Callable[[Any], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        skip_nulls: bool = True,
        pass_name: bool = False,
        strategy: MapElementsStrategy = "thread_local",
    ) -> Self:
        """
        Apply a custom/user-defined function (UDF) in a GroupBy or Projection context.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`Expr.map_elements`.

        Parameters
        ----------
        function
            Lambda/ function to apply.
        return_dtype
            Dtype of the output Series.
            If not set, the dtype will be
            ``polars.Unknown``.
        skip_nulls
            Don't apply the function over values
            that contain nulls. This is faster.
        pass_name
            Pass the Series name to the custom function
            This is more expensive.
        strategy : {'thread_local', 'threading'}
            This functionality is in `alpha` stage. This may be removed
            /changed without it being considered a breaking change.

            - 'thread_local': run the python function on a single thread.
            - 'threading': run the python function on separate threads. Use with
                        care as this can slow performance. This might only speed up
                        your code if the amount of work per element is significant
                        and the python function releases the GIL (e.g. via calling
                        a c function)

        """
        return self.map_elements(
            function,
            return_dtype=return_dtype,
            skip_nulls=skip_nulls,
            pass_name=pass_name,
            strategy=strategy,
        )
