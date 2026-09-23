    def _numba_agg_general(
        self,
        func: Callable,
        engine_kwargs: dict[str, bool] | None,
        numba_cache_key_str: str,
        *aggregator_args,
    ):
        """
        Perform groupby with a standard numerical aggregation function (e.g. mean)
        with Numba.
        """
        if not self.as_index:
            raise NotImplementedError(
                "as_index=False is not supported. Use .reset_index() instead."
            )
        if self.axis == 1:
            raise NotImplementedError("axis=1 is not supported.")

        with self._group_selection_context():
            data = self._selected_obj
        df = data if data.ndim == 2 else data.to_frame()
        starts, ends, sorted_index, sorted_data = self._numba_prep(func, df)
        aggregator = executor.generate_shared_aggregator(
            func, engine_kwargs, numba_cache_key_str
        )
        result = aggregator(sorted_data, starts, ends, 0, *aggregator_args)

        cache_key = (func, numba_cache_key_str)
        if cache_key not in NUMBA_FUNC_CACHE:
            NUMBA_FUNC_CACHE[cache_key] = aggregator

        index = self.grouper.result_index
        if data.ndim == 1:
            result_kwargs = {"name": data.name}
            result = result.ravel()
        else:
            result_kwargs = {"columns": data.columns}
        return data._constructor(result, index=index, **result_kwargs)
