    def fillna(self, value, limit=None, inplace=False, downcast=None):
        """ fillna on the block with the value. If we fail, then convert to
        ObjectBlock and try again
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        mask = isna(self.values)
        if limit is not None:
            limit = libalgos._validate_limit(None, limit=limit)
            mask[mask.cumsum(self.ndim - 1) > limit] = False

        if not self._can_hold_na:
            if inplace:
                return self
            else:
                return self.copy()

        if self._can_hold_element(value):
            # equivalent: _try_coerce_args(value) would not raise
            blocks = self.putmask(mask, value, inplace=inplace)
            return self._maybe_downcast(blocks, downcast)

        # we can't process the value, but nothing to do
        if not mask.any():
            return self if inplace else self.copy()

        # operate column-by-column
        def f(mask, val, idx):
            block = self.coerce_to_target_dtype(value)

            # slice out our block
            if idx is not None:
                # i.e. self.ndim == 2
                block = block.getitem_block(slice(idx, idx + 1))
            return block.fillna(value, limit=limit, inplace=inplace, downcast=None)

        return self.split_and_operate(None, f, inplace)
