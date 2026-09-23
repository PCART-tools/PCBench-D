    def fillna(self, value, limit=None, inplace=False, downcast=None):
        """ fillna on the block with the value. If we fail, then convert to
        ObjectBlock and try again
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')

        if not self._can_hold_na:
            if inplace:
                return self
            else:
                return self.copy()

        mask = isna(self.values)
        if limit is not None:
            if not is_integer(limit):
                raise ValueError('Limit must be an integer')
            if limit < 1:
                raise ValueError('Limit must be greater than 0')
            if self.ndim > 2:
                raise NotImplementedError("number of dimensions for 'fillna' "
                                          "is currently limited to 2")
            mask[mask.cumsum(self.ndim - 1) > limit] = False

        # fillna, but if we cannot coerce, then try again as an ObjectBlock
        try:
            values, _ = self._try_coerce_args(self.values, value)
            blocks = self.putmask(mask, value, inplace=inplace)
            blocks = [b.make_block(values=self._try_coerce_result(b.values))
                      for b in blocks]
            return self._maybe_downcast(blocks, downcast)
        except (TypeError, ValueError):

            # we can't process the value, but nothing to do
            if not mask.any():
                return self if inplace else self.copy()

            # operate column-by-column
            def f(m, v, i):
                block = self.coerce_to_target_dtype(value)

                # slice out our block
                if i is not None:
                    block = block.getitem_block(slice(i, i + 1))
                return block.fillna(value,
                                    limit=limit,
                                    inplace=inplace,
                                    downcast=None)

            return self.split_and_operate(mask, f, inplace)
