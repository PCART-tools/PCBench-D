    def _numba_apply(
        self,
        func: Callable[..., Any],
        numba_cache_key_str: str,
        engine_kwargs: dict[str, bool] | None = None,
        *func_args,
    ):
        window_indexer = self._get_window_indexer()
        min_periods = (
            self.min_periods
            if self.min_periods is not None
            else window_indexer.window_size
        )
        obj = self._create_data(self._selected_obj)
        if self.axis == 1:
            obj = obj.T
        values = self._prep_values(obj.to_numpy())
        if values.ndim == 1:
            values = values.reshape(-1, 1)
        start, end = window_indexer.get_window_bounds(
            num_values=len(values),
            min_periods=min_periods,
            center=self.center,
            closed=self.closed,
        )
        self._check_window_bounds(start, end, len(values))
        aggregator = executor.generate_shared_aggregator(
            func, engine_kwargs, numba_cache_key_str
        )
        result = aggregator(values, start, end, min_periods, *func_args)
        NUMBA_FUNC_CACHE[(func, numba_cache_key_str)] = aggregator
        result = result.T if self.axis == 1 else result
        if obj.ndim == 1:
            result = result.squeeze()
            out = obj._constructor(result, index=obj.index, name=obj.name)
            return out
        else:
            out = obj._constructor(result, index=obj.index, columns=obj.columns)
            return self._resolve_output(out, obj)
