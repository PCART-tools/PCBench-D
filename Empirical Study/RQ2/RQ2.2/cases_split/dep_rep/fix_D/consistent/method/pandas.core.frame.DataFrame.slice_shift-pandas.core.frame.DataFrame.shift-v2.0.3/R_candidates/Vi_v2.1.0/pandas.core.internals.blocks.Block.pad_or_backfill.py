    def pad_or_backfill(
        self,
        *,
        method: FillnaOptions,
        axis: AxisInt = 0,
        inplace: bool = False,
        limit: int | None = None,
        limit_area: Literal["inside", "outside"] | None = None,
        downcast: Literal["infer"] | None = None,
        using_cow: bool = False,
    ) -> list[Block]:
        if not self._can_hold_na:
            # If there are no NAs, then interpolate is a no-op
            if using_cow:
                return [self.copy(deep=False)]
            return [self] if inplace else [self.copy()]

        copy, refs = self._get_refs_and_copy(using_cow, inplace)

        # Dispatch to the NumpyExtensionArray method.
        # We know self.array_values is a NumpyExtensionArray bc EABlock overrides
        vals = cast(NumpyExtensionArray, self.array_values)
        if axis == 1:
            vals = vals.T
        new_values = vals._pad_or_backfill(
            method=method,
            limit=limit,
            limit_area=limit_area,
            copy=copy,
        )
        if axis == 1:
            new_values = new_values.T

        data = extract_array(new_values, extract_numpy=True)

        nb = self.make_block_same_class(data, refs=refs)
        return nb._maybe_downcast([nb], downcast, using_cow)
