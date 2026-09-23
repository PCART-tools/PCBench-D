    @final
    def _aggregate_with_numba(self, func, *args, engine_kwargs=None, **kwargs):
        """
        Perform groupby aggregation routine with the numba engine.

        This routine mimics the data splitting routine of the DataSplitter class
        to generate the indices of each group in the sorted data and then passes the
        data and indices into a Numba jitted function.
        """
        data = self._obj_with_exclusions
        df = data if data.ndim == 2 else data.to_frame()

        starts, ends, sorted_index, sorted_data = self._numba_prep(df)
        numba_.validate_udf(func)
        numba_agg_func = numba_.generate_numba_agg_func(
            func, **get_jit_arguments(engine_kwargs, kwargs)
        )
        result = numba_agg_func(
            sorted_data,
            sorted_index,
            starts,
            ends,
            len(df.columns),
            *args,
        )
        index = self.grouper.result_index
        if data.ndim == 1:
            result_kwargs = {"name": data.name}
            result = result.ravel()
        else:
            result_kwargs = {"columns": data.columns}
        res = data._constructor(result, index=index, **result_kwargs)
        if not self.as_index:
            res = self._insert_inaxis_grouper(res)
            res.index = default_index(len(res))
        return res
