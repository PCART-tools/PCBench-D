    def _numba_apply(
        self,
        func: Callable[..., Any],
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
            step=self.step,
        )
        self._check_window_bounds(start, end, len(values))
        aggregator = executor.generate_shared_aggregator(
            func, **get_jit_arguments(engine_kwargs)
        )
        result = aggregator(values, start, end, min_periods, *func_args)
        result = result.T if self.axis == 1 else result
        index = self._slice_axis_for_step(obj.index, result)
        if obj.ndim == 1:
            result = result.squeeze()
            out = obj._constructor(result, index=index, name=obj.name)
            return out
        else:
            columns = self._slice_axis_for_step(obj.columns, result.T)
            out = obj._constructor(result, index=index, columns=columns)
            return self._resolve_output(out, obj)
