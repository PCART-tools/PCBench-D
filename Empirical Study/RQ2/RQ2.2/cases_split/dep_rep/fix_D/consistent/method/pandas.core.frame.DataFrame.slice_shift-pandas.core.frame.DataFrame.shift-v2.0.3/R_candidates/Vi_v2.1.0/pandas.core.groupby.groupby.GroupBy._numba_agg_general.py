    def _numba_agg_general(
        self,
        func: Callable,
        dtype_mapping: dict[np.dtype, Any],
        engine_kwargs: dict[str, bool] | None,
        **aggregator_kwargs,
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

        data = self._obj_with_exclusions
        df = data if data.ndim == 2 else data.to_frame()

        aggregator = executor.generate_shared_aggregator(
            func,
            dtype_mapping,
            True,  # is_grouped_kernel
            **get_jit_arguments(engine_kwargs),
        )
        # Pass group ids to kernel directly if it can handle it
        # (This is faster since it doesn't require a sort)
        ids, _, _ = self.grouper.group_info
        ngroups = self.grouper.ngroups

        res_mgr = df._mgr.apply(
            aggregator, labels=ids, ngroups=ngroups, **aggregator_kwargs
        )
        res_mgr.axes[1] = self.grouper.result_index
        result = df._constructor_from_mgr(res_mgr, axes=res_mgr.axes)

        if data.ndim == 1:
            result = result.squeeze("columns")
            result.name = data.name
        else:
            result.columns = data.columns
        return result
