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
        if isinstance(values, BaseMaskedArray):
            return self._masked_ea_wrap_cython_operation(
                values,
                min_count=min_count,
                ngroups=ngroups,
                comp_ids=comp_ids,
                **kwargs,
            )

        elif isinstance(values, Categorical):
            assert self.how == "rank"  # the only one implemented ATM
            assert values.ordered  # checked earlier
            mask = values.isna()
            npvalues = values._ndarray

            res_values = self._cython_op_ndim_compat(
                npvalues,
                min_count=min_count,
                ngroups=ngroups,
                comp_ids=comp_ids,
                mask=mask,
                **kwargs,
            )

            # If we ever have more than just "rank" here, we'll need to do
            #  `if self.how in self.cast_blocklist` like we do for other dtypes.
            return res_values

        npvalues = self._ea_to_cython_values(values)

        res_values = self._cython_op_ndim_compat(
            npvalues,
            min_count=min_count,
            ngroups=ngroups,
            comp_ids=comp_ids,
            mask=None,
            **kwargs,
        )

        if self.how in self.cast_blocklist:
            # i.e. how in ["rank"], since other cast_blocklist methods don't go
            #  through cython_operation
            return res_values

        return self._reconstruct_ea_result(values, res_values)
