    def where(
        self,
        other,
        cond,
        align=True,
        errors="raise",
        try_cast: bool = False,
        axis: int = 0,
    ) -> List["Block"]:
        """
        evaluate the block; return result block(s) from the result

        Parameters
        ----------
        other : a ndarray/object
        cond  : the condition to respect
        align : boolean, perform alignment on other/cond
        errors : str, {'raise', 'ignore'}, default 'raise'
            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object
        axis : int

        Returns
        -------
        a new block(s), the result of the func
        """
        import pandas.core.computation.expressions as expressions

        assert errors in ["raise", "ignore"]
        transpose = self.ndim == 2

        values = self.values
        orig_other = other
        if transpose:
            values = values.T

        other = getattr(other, "_values", getattr(other, "values", other))
        cond = getattr(cond, "values", cond)

        # If the default broadcasting would go in the wrong direction, then
        # explicitly reshape other instead
        if getattr(other, "ndim", 0) >= 1:
            if values.ndim - 1 == other.ndim and axis == 1:
                other = other.reshape(tuple(other.shape + (1,)))
            elif transpose and values.ndim == self.ndim - 1:
                cond = cond.T

        if not hasattr(cond, "shape"):
            raise ValueError("where must have a condition that is ndarray like")

        # our where function
        def func(cond, values, other):

            if not (
                (self.is_integer or self.is_bool)
                and lib.is_float(other)
                and np.isnan(other)
            ):
                # np.where will cast integer array to floats in this case
                if not self._can_hold_element(other):
                    raise TypeError
                if lib.is_scalar(other) and isinstance(values, np.ndarray):
                    other = convert_scalar(values, other)

            fastres = expressions.where(cond, values, other)
            return fastres

        if cond.ravel().all():
            result = values
        else:
            # see if we can operate on the entire block, or need item-by-item
            # or if we are a single block (ndim == 1)
            try:
                result = func(cond, values, other)
            except TypeError:

                # we cannot coerce, return a compat dtype
                # we are explicitly ignoring errors
                block = self.coerce_to_target_dtype(other)
                blocks = block.where(
                    orig_other,
                    cond,
                    align=align,
                    errors=errors,
                    try_cast=try_cast,
                    axis=axis,
                )
                return self._maybe_downcast(blocks, "infer")

        if self._can_hold_na or self.ndim == 1:

            if transpose:
                result = result.T

            return [self.make_block(result)]

        # might need to separate out blocks
        axis = cond.ndim - 1
        cond = cond.swapaxes(axis, 0)
        mask = np.array([cond[i].all() for i in range(cond.shape[0])], dtype=bool)

        result_blocks = []
        for m in [mask, ~mask]:
            if m.any():
                taken = result.take(m.nonzero()[0], axis=axis)
                r = maybe_downcast_numeric(taken, self.dtype)
                nb = self.make_block(r.T, placement=self.mgr_locs[m])
                result_blocks.append(nb)

        return result_blocks
