    @final
    def interpolate(
        self,
        *,
        method: InterpolateOptions,
        index: Index,
        inplace: bool = False,
        limit: int | None = None,
        limit_direction: Literal["forward", "backward", "both"] = "forward",
        limit_area: Literal["inside", "outside"] | None = None,
        downcast: Literal["infer"] | None = None,
        using_cow: bool = False,
        **kwargs,
    ) -> list[Block]:
        inplace = validate_bool_kwarg(inplace, "inplace")
        # error: Non-overlapping equality check [...]
        if method == "asfreq":  # type: ignore[comparison-overlap]
            # clean_fill_method used to allow this
            missing.clean_fill_method(method)

        if not self._can_hold_na:
            # If there are no NAs, then interpolate is a no-op
            if using_cow:
                return [self.copy(deep=False)]
            return [self] if inplace else [self.copy()]

        # TODO(3.0): this case will not be reachable once GH#53638 is enforced
        if self.dtype == _dtype_obj:
            # only deal with floats
            # bc we already checked that can_hold_na, we don't have int dtype here
            # test_interp_basic checks that we make a copy here
            if using_cow:
                return [self.copy(deep=False)]
            return [self] if inplace else [self.copy()]

        copy, refs = self._get_refs_and_copy(using_cow, inplace)

        # Dispatch to the EA method.
        new_values = self.array_values.interpolate(
            method=method,
            axis=self.ndim - 1,
            index=index,
            limit=limit,
            limit_direction=limit_direction,
            limit_area=limit_area,
            copy=copy,
            **kwargs,
        )
        data = extract_array(new_values, extract_numpy=True)

        nb = self.make_block_same_class(data, refs=refs)
        return nb._maybe_downcast([nb], downcast, using_cow)
