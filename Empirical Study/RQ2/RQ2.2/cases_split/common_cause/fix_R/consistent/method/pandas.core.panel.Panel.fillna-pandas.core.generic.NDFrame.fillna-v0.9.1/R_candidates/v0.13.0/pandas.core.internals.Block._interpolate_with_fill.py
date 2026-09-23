    def _interpolate_with_fill(self, method='pad', axis=0, inplace=False,
                               limit=None, fill_value=None, coerce=False,
                               downcast=None):
        """ fillna but using the interpolate machinery """

        # if we are coercing, then don't force the conversion
        # if the block can't hold the type
        if coerce:
            if not self._can_hold_na:
                if inplace:
                    return [self]
                else:
                    return [self.copy()]

        fill_value = self._try_fill(fill_value)
        values = self.values if inplace else self.values.copy()
        values = self._try_operate(values)
        values = com.interpolate_2d(values, method, axis, limit, fill_value)
        values = self._try_coerce_result(values)

        blocks = [make_block(values, self.items, self.ref_items,
                             ndim=self.ndim, klass=self.__class__,
                             fastpath=True)]
        return self._maybe_downcast(blocks, downcast)
