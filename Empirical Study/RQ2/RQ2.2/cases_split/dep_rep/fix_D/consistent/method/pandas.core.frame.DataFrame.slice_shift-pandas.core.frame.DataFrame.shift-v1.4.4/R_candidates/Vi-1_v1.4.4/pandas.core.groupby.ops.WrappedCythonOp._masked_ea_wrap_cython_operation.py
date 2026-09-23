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

        # Copy to ensure input and result masks don't end up shared
        mask = values._mask.copy()
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

        dtype = self._get_result_dtype(orig_values.dtype)
        assert isinstance(dtype, BaseMaskedDtype)
        cls = dtype.construct_array_type()

        if self.kind != "aggregate":
            return cls(res_values.astype(dtype.type, copy=False), mask)
        else:
            return cls(res_values.astype(dtype.type, copy=False), result_mask)
