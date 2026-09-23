    @final
    def _aggregate_with_numba(self, data, func, *args, engine_kwargs=None, **kwargs):
        """
        Perform groupby aggregation routine with the numba engine.

        This routine mimics the data splitting routine of the DataSplitter class
        to generate the indices of each group in the sorted data and then passes the
        data and indices into a Numba jitted function.
        """
        starts, ends, sorted_index, sorted_data = self._numba_prep(data)
        numba_.validate_udf(func)
        numba_agg_func = numba_.generate_numba_agg_func(
            func, **get_jit_arguments(engine_kwargs, kwargs)
        )
        result = numba_agg_func(
            sorted_data,
            sorted_index,
            starts,
            ends,
            len(data.columns),
            *args,
        )
        return result
