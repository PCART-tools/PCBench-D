    @final
    def _masked_ea_wrap_cython_operation(
        self,
        values: BaseMaskedArray,
        min_count: int,
        ngroups: int,
        comp_ids: np.ndarray,
        **kwargs,
    ) -> BaseMaskedArray:
        """
        Equivalent of `_ea_wrap_cython_operation`, but optimized for masked EA's
        and cython algorithms which accept a mask.
        """
        orig_values = values

        # libgroupby functions are responsible for NOT altering mask
        mask = values._mask
        if self.kind != "aggregate":
            result_mask = mask.copy()
        else:
            result_mask = np.zeros(ngroups, dtype=bool)

        arr = values._data

        res_values = self._cython_op_ndim_compat(
            arr,
            min_count=min_count,
            ngroups=ngroups,
            comp_ids=comp_ids,
            mask=mask,
            result_mask=result_mask,
            **kwargs,
        )

        if self.how == "ohlc":
            result_mask = np.tile(result_mask, (4, 1)).T

        # res_values should already have the correct dtype, we just need to
        #  wrap in a MaskedArray
        return orig_values._maybe_mask_result(res_values, result_mask)
