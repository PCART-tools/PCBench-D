    def fillna(
        self, value, limit=None, inplace: bool = False, downcast=None
    ) -> list[Block]:
        """
        fillna on the block with the value. If we fail, then convert to
        ObjectBlock and try again
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        mask = isna(self.values)
        mask, noop = validate_putmask(self.values, mask)

        if limit is not None:
            limit = libalgos.validate_limit(None, limit=limit)
            mask[mask.cumsum(self.ndim - 1) > limit] = False

        if not self._can_hold_na:
            if inplace:
                return [self]
            else:
                return [self.copy()]

        if self._can_hold_element(value):
            nb = self if inplace else self.copy()
            putmask_inplace(nb.values, mask, value)
            return nb._maybe_downcast([nb], downcast)

        if noop:
            # we can't process the value, but nothing to do
            return [self] if inplace else [self.copy()]

        elif self.ndim == 1 or self.shape[0] == 1:
            blk = self.coerce_to_target_dtype(value)
            # bc we have already cast, inplace=True may avoid an extra copy
            return blk.fillna(value, limit=limit, inplace=True, downcast=None)

        else:
            # operate column-by-column
            return self.split_and_operate(
                type(self).fillna, value, limit=limit, inplace=inplace, downcast=None
            )
