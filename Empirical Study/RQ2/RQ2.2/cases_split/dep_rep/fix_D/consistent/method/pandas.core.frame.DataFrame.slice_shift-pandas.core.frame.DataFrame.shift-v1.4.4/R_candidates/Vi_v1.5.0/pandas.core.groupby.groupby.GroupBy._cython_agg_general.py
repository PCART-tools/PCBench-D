    @final
    def _cython_agg_general(
        self,
        how: str,
        alt: Callable,
        numeric_only: bool | lib.NoDefault,
        min_count: int = -1,
        ignore_failures: bool = True,
        **kwargs,
    ):
        # Note: we never get here with how="ohlc" for DataFrameGroupBy;
        #  that goes through SeriesGroupBy
        numeric_only_bool = self._resolve_numeric_only(how, numeric_only, axis=0)

        data = self._get_data_to_aggregate()
        is_ser = data.ndim == 1

        orig_len = len(data)
        if numeric_only_bool:
            if is_ser and not is_numeric_dtype(self._selected_obj.dtype):
                # GH#41291 match Series behavior
                kwd_name = "numeric_only"
                if how in ["any", "all"]:
                    kwd_name = "bool_only"
                raise NotImplementedError(
                    f"{type(self).__name__}.{how} does not implement {kwd_name}."
                )
            elif not is_ser:
                data = data.get_numeric_data(copy=False)

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

        # TypeError -> we may have an exception in trying to aggregate
        #  continue and exclude the block
        new_mgr = data.grouped_reduce(array_func, ignore_failures=ignore_failures)

        if not is_ser and len(new_mgr) < orig_len:
            warn_dropping_nuisance_columns_deprecated(type(self), how, numeric_only)

        res = self._wrap_agged_manager(new_mgr)
        if is_ser:
            res.index = self.grouper.result_index
            return self._reindex_output(res)
        else:
            return res
