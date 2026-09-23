    @final
    def _cython_agg_general(
        self,
        how: str,
        alt: Callable,
        numeric_only: bool = False,
        min_count: int = -1,
        **kwargs,
    ):
        # Note: we never get here with how="ohlc" for DataFrameGroupBy;
        #  that goes through SeriesGroupBy

        data = self._get_data_to_aggregate(numeric_only=numeric_only, name=how)

        def array_func(values: ArrayLike) -> ArrayLike:
            try:
                result = self.grouper._cython_operation(
                    "aggregate",
                    values,
                    how,
                    axis=data.ndim - 1,
                    min_count=min_count,
                    **kwargs,
                )
            except NotImplementedError:
                # generally if we have numeric_only=False
                # and non-applicable functions
                # try to python agg
                # TODO: shouldn't min_count matter?
                result = self._agg_py_fallback(values, ndim=data.ndim, alt=alt)

            return result

        new_mgr = data.grouped_reduce(array_func)
        res = self._wrap_agged_manager(new_mgr)
        out = self._wrap_aggregated_output(res)
        if self.axis == 1:
            out = out.infer_objects(copy=False)
        return out
