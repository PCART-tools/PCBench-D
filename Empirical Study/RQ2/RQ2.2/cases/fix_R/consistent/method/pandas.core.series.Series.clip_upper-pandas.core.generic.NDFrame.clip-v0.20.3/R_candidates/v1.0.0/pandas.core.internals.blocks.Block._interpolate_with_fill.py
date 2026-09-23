    def _interpolate_with_fill(
        self,
        method="pad",
        axis=0,
        inplace=False,
        limit=None,
        fill_value=None,
        coerce=False,
        downcast=None,
    ):
        """ fillna but using the interpolate machinery """

        inplace = validate_bool_kwarg(inplace, "inplace")

        # if we are coercing, then don't force the conversion
        # if the block can't hold the type
        if coerce:
            if not self._can_hold_na:
                if inplace:
                    return [self]
                else:
                    return [self.copy()]

        values = self.values if inplace else self.values.copy()

        # We only get here for non-ExtensionBlock
        fill_value = convert_scalar(self.values, fill_value)

        values = missing.interpolate_2d(
            values,
            method=method,
            axis=axis,
            limit=limit,
            fill_value=fill_value,
            dtype=self.dtype,
        )

        blocks = [self.make_block_same_class(values, ndim=self.ndim)]
        return self._maybe_downcast(blocks, downcast)
