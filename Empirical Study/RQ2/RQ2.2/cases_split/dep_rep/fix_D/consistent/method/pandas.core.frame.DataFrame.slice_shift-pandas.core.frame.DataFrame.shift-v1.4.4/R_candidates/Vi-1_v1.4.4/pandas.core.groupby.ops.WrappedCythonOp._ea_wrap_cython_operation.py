    @final
    def _ea_wrap_cython_operation(
        self,
        values: ExtensionArray,
        min_count: int,
        ngroups: int,
        comp_ids: np.ndarray,
        **kwargs,
    ) -> ArrayLike:
        """
        If we have an ExtensionArray, unwrap, call _cython_operation, and
        re-wrap if appropriate.
        """
        # TODO: general case implementation overridable by EAs.
        if isinstance(values, BaseMaskedArray) and self.uses_mask():
            return self._masked_ea_wrap_cython_operation(
                values,
                min_count=min_count,
                ngroups=ngroups,
                comp_ids=comp_ids,
                **kwargs,
            )

        if isinstance(values, (DatetimeArray, PeriodArray, TimedeltaArray)):
            # All of the functions implemented here are ordinal, so we can
            #  operate on the tz-naive equivalents
            npvalues = values._ndarray.view("M8[ns]")
        elif isinstance(values.dtype, (BooleanDtype, _IntegerDtype)):
            # IntegerArray or BooleanArray
            npvalues = values.to_numpy("float64", na_value=np.nan)
        elif isinstance(values.dtype, FloatingDtype):
            # FloatingArray
            npvalues = values.to_numpy(values.dtype.numpy_dtype, na_value=np.nan)
        elif isinstance(values.dtype, StringDtype):
            # StringArray
            npvalues = values.to_numpy(object, na_value=np.nan)
        else:
            raise NotImplementedError(
                f"function is not implemented for this dtype: {values.dtype}"
            )

        res_values = self._cython_op_ndim_compat(
            npvalues,
            min_count=min_count,
            ngroups=ngroups,
            comp_ids=comp_ids,
            mask=None,
            **kwargs,
        )

        if self.how in ["rank"]:
            # i.e. how in WrappedCythonOp.cast_blocklist, since
            #  other cast_blocklist methods dont go through cython_operation
            return res_values

        return self._reconstruct_ea_result(values, res_values)
